from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union
import requests
from requests.auth import HTTPBasicAuth
import mysql.connector
from mysql.connector import Error
import json
import logging
import uuid
from datetime import datetime, timezone
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
import os
from pathlib import Path
import subprocess
import tempfile
import pytz
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:80",
        "http://127.0.0.1:80",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],  # Vue dev server and production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store for background tasks
background_tasks_store: Dict[str, Dict[str, Any]] = {}
executor = ThreadPoolExecutor(max_workers=5)

# Create backups directory if it doesn't exist
BACKUPS_DIR = Path("backups")
BACKUPS_DIR.mkdir(exist_ok=True)


class JiraSyncRequest(BaseModel):
    # Jira configuration
    jira_domain: str  # e.g., "your-domain.atlassian.net"
    jira_email: str
    jira_api_token: str
    jql: str  # e.g., "project = SAC"
    fields: Union[List[str], Dict[str, str]]  # Can be list of fields or dict for mapping
    
    # MySQL configuration
    mysql_host: str
    mysql_port: int = 3306
    mysql_user: str
    mysql_password: str
    mysql_database: str
    mysql_table: str
    
    # Optional pagination settings
    max_results_per_page: int = 50


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "jira-sync-backend"}


@app.post("/sync-jira-issues")
async def sync_jira_issues(sync_request: JiraSyncRequest):
    """
    Start synchronization of Jira issues to MySQL database in background
    """
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Initialize task status
    background_tasks_store[task_id] = {
        "id": task_id,
        "status": "iniciando",
        "progress": 0,
        "total_issues": 0,
        "processed_issues": 0,
        "message": "Iniciando sincronización...",
        "started_at": datetime.now().isoformat(),
        "completed_at": None,
        "error": None,
        "result": None
    }
    
    # Start background task
    loop = asyncio.get_event_loop()
    loop.run_in_executor(
        executor,
        run_sync_task,
        task_id,
        sync_request.dict()
    )
    
    return {
        "task_id": task_id,
        "message": "Sincronización iniciada en segundo plano",
        "status_url": f"/sync-status/{task_id}"
    }


def run_sync_task(task_id: str, sync_request_dict: dict):
    """Run the sync task in background thread"""
    try:
        # Create async event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the async sync function
        result = loop.run_until_complete(
            sync_jira_issues_background(task_id, sync_request_dict)
        )
        
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Error in background task {task_id}: {str(e)}")
        background_tasks_store[task_id].update({
            "status": "error",
            "error": str(e),
            "completed_at": datetime.now().isoformat()
        })


async def sync_jira_issues_background(task_id: str, sync_request_dict: dict):
    """
    Synchronize Jira issues to MySQL database with progress tracking
    """
    try:
        # Recreate the request object
        sync_request = JiraSyncRequest(**sync_request_dict)
        
        # Step 1: Get approximate count of issues
        background_tasks_store[task_id]["status"] = "obteniendo_total"
        background_tasks_store[task_id]["message"] = "Obteniendo cantidad total de issues..."
        
        issue_count = await get_issue_count(sync_request)
        background_tasks_store[task_id]["total_issues"] = issue_count
        background_tasks_store[task_id]["message"] = f"Se encontraron {issue_count} issues"
        
        # Step 2: Connect to MySQL
        background_tasks_store[task_id]["status"] = "conectando_db"
        background_tasks_store[task_id]["message"] = "Conectando a MySQL..."
        connection = connect_to_mysql(sync_request)
        
        # Ensure logs table exists
        ensure_logs_table_exists(connection)
        
        # Save initial log entry
        save_sync_log(connection, task_id, sync_request, "iniciando", issue_count)
        
        # Step 3: Fetch all issues with pagination and progress tracking
        background_tasks_store[task_id]["status"] = "descargando"
        background_tasks_store[task_id]["message"] = "Descargando issues de Jira..."
        
        all_issues = await fetch_all_issues_with_progress(sync_request, issue_count, task_id)
        
        # Step 4: Ensure table exists
        background_tasks_store[task_id]["status"] = "preparando_tabla"
        background_tasks_store[task_id]["message"] = "Preparando tabla en MySQL..."
        ensure_table_exists(connection, sync_request, all_issues)
        
        # Step 5: Sync issues to database
        background_tasks_store[task_id]["status"] = "sincronizando"
        background_tasks_store[task_id]["message"] = "Sincronizando issues a la base de datos..."
        
        synced_count = sync_issues_to_database_with_progress(
            connection, sync_request, all_issues, task_id
        )
        
        # Step 6: Generate backup SQL file
        background_tasks_store[task_id]["status"] = "generando_respaldo"
        background_tasks_store[task_id]["message"] = "Generando archivo de respaldo SQL..."
        logger.info(f"Task {task_id}: Iniciando generación de backup...")
        
        backup_filename = await generate_backup(task_id, sync_request, sync_request.mysql_table, issue_count)
        
        # Generate download URL for backup
        backup_url = f"/backups/{backup_filename}" if backup_filename else None
        
        # Save final log entry
        result_data = {
            "total_issues": len(all_issues),
            "synced_issues": synced_count,
            "approximate_count": issue_count,
            "backup_file": backup_filename,
            "backup_url": backup_url
        }
        save_sync_log(connection, task_id, sync_request, "completado", 
                     len(all_issues), synced_count, None, result_data, backup_filename)
        
        # Close connection
        connection.close()
        
        # Update final status
        background_tasks_store[task_id].update({
            "status": "completado",
            "progress": 100,
            "processed_issues": synced_count,
            "message": f"Sincronización completada: {synced_count} issues procesados. Backup: {backup_filename}",
            "completed_at": datetime.now().isoformat(),
            "result": result_data,
            "backup_file": backup_filename,
            "backup_url": backup_url
        })
        
        logger.info(f"Task {task_id}: Sincronización completada exitosamente con backup: {backup_filename}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during sync task {task_id}: {str(e)}")
        
        # Try to save error log if connection exists
        try:
            if 'connection' in locals() and connection:
                save_sync_log(connection, task_id, sync_request, "error", 
                            0, 0, str(e), None, None)
                connection.close()
        except:
            pass
        
        background_tasks_store[task_id].update({
            "status": "error",
            "error": str(e),
            "message": f"Error: {str(e)}",
            "completed_at": datetime.now().isoformat()
        })
        raise


async def get_issue_count(sync_request: JiraSyncRequest) -> int:
    """Get approximate count of issues matching the JQL"""
    url = f"https://{sync_request.jira_domain}/rest/api/3/search/approximate-count"
    auth = HTTPBasicAuth(sync_request.jira_email, sync_request.jira_api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {"jql": sync_request.jql}
    
    response = requests.post(url, json=payload, headers=headers, auth=auth)
    response.raise_for_status()
    
    return response.json().get("count", 0)


async def fetch_all_issues_with_progress(sync_request: JiraSyncRequest, total_count: int, task_id: str) -> List[Dict[str, Any]]:
    """Fetch all issues using pagination with progress tracking"""
    all_issues = []
    next_page_token = None
    
    url = f"https://{sync_request.jira_domain}/rest/api/3/search/jql"
    auth = HTTPBasicAuth(sync_request.jira_email, sync_request.jira_api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Extract field names for Jira API
    if isinstance(sync_request.fields, dict):
        jira_fields = list(sync_request.fields.keys())
    else:
        jira_fields = sync_request.fields
    
    while True:
        payload = {
            "jql": sync_request.jql,
            "fields": jira_fields,
            "maxResults": sync_request.max_results_per_page
        }
        
        if next_page_token:
            payload["nextPageToken"] = next_page_token
        
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        
        data = response.json()
        issues = data.get("issues", [])
        all_issues.extend(issues)
        
        # Update progress
        progress = min(int((len(all_issues) / total_count) * 50), 50)  # 0-50% for downloading
        background_tasks_store[task_id].update({
            "progress": progress,
            "message": f"Descargando issues: {len(all_issues)}/{total_count}"
        })
        
        logger.info(f"Task {task_id}: Fetched {len(all_issues)}/{total_count} issues")
        
        # Check if there are more pages
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
    
    return all_issues


def connect_to_mysql(sync_request: JiraSyncRequest) -> mysql.connector.MySQLConnection:
    """Create MySQL connection"""
    try:
        connection = mysql.connector.connect(
            host=sync_request.mysql_host,
            port=sync_request.mysql_port,
            user=sync_request.mysql_user,
            password=sync_request.mysql_password,
            database=sync_request.mysql_database
        )
        return connection
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        raise


def ensure_logs_table_exists(connection: mysql.connector.MySQLConnection) -> None:
    """Ensure logs table exists for tracking sync history"""
    cursor = connection.cursor()
    
    create_logs_table_sql = """
    CREATE TABLE IF NOT EXISTS sync_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_id VARCHAR(255) UNIQUE NOT NULL,
        started_at TIMESTAMP NOT NULL,
        completed_at TIMESTAMP NULL,
        status VARCHAR(50) NOT NULL,
        jql_query TEXT NOT NULL,
        total_issues INT DEFAULT 0,
        processed_issues INT DEFAULT 0,
        error_message TEXT NULL,
        result JSON NULL,
        backup_file VARCHAR(255) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_task_id (task_id),
        INDEX idx_status (status),
        INDEX idx_started_at (started_at)
    )
    """
    
    try:
        cursor.execute(create_logs_table_sql)
        connection.commit()
        logger.info("Logs table ensured")
    except Error as e:
        logger.warning(f"Could not create logs table: {e}")
    finally:
        cursor.close()


def save_sync_log(connection: mysql.connector.MySQLConnection, task_id: str, 
                  sync_request: JiraSyncRequest, status: str, 
                  total_issues: int = 0, processed_issues: int = 0,
                  error_message: str = None, result: dict = None,
                  backup_file: str = None) -> None:
    """Save sync task information to logs table"""
    cursor = connection.cursor()
    
    task_info = background_tasks_store.get(task_id, {})
    
    # First, try with the simpler table structure (without config column)
    insert_log_sql = """
    INSERT INTO sync_logs (task_id, started_at, completed_at, status, jql_query,
                          total_issues, processed_issues, error_message, result, backup_file)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        completed_at = VALUES(completed_at),
        status = VALUES(status),
        total_issues = VALUES(total_issues),
        processed_issues = VALUES(processed_issues),
        error_message = VALUES(error_message),
        result = VALUES(result),
        backup_file = VALUES(backup_file)
    """
    
    values = (
        task_id,
        task_info.get("started_at", datetime.now().isoformat()),
        task_info.get("completed_at"),
        status,
        sync_request.jql,
        total_issues,
        processed_issues,
        error_message,
        json.dumps(result) if result else None,
        backup_file
    )
    
    try:
        cursor.execute(insert_log_sql, values)
        connection.commit()
        logger.info(f"Saved log for task {task_id} with status {status}")
    except Error as e:
        # If the simple insert fails, it might be because we need to add the config column
        if "Unknown column" not in str(e):
            logger.error(f"Error saving log for task {task_id}: {e}")
        else:
            # Try to add the config column
            try:
                alter_sql = "ALTER TABLE sync_logs ADD COLUMN config JSON NULL AFTER jql_query"
                cursor.execute(alter_sql)
                connection.commit()
                logger.info("Added config column to sync_logs table")
                
                # Now try with config
                config_data = {
                    "jira_domain": sync_request.jira_domain,
                    "jira_email": sync_request.jira_email,
                    "jql": sync_request.jql,
                    "fields": sync_request.fields,
                    "mysql_host": sync_request.mysql_host,
                    "mysql_port": sync_request.mysql_port,
                    "mysql_database": sync_request.mysql_database,
                    "mysql_table": sync_request.mysql_table,
                    "max_results_per_page": sync_request.max_results_per_page
                }
                
                insert_with_config_sql = """
                INSERT INTO sync_logs (task_id, started_at, completed_at, status, jql_query, config,
                                      total_issues, processed_issues, error_message, result, backup_file)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    completed_at = VALUES(completed_at),
                    status = VALUES(status),
                    config = VALUES(config),
                    total_issues = VALUES(total_issues),
                    processed_issues = VALUES(processed_issues),
                    error_message = VALUES(error_message),
                    result = VALUES(result),
                    backup_file = VALUES(backup_file)
                """
                
                values_with_config = (
                    task_id,
                    task_info.get("started_at", datetime.now().isoformat()),
                    task_info.get("completed_at"),
                    status,
                    sync_request.jql,
                    json.dumps(config_data),
                    total_issues,
                    processed_issues,
                    error_message,
                    json.dumps(result) if result else None,
                    backup_file
                )
                
                cursor.execute(insert_with_config_sql, values_with_config)
                connection.commit()
                logger.info(f"Saved log with config for task {task_id}")
            except Error as e2:
                logger.error(f"Error adding config column or saving log: {e2}")
    finally:
        cursor.close()


async def generate_backup(task_id: str, config: JiraSyncRequest, table_name: str, total_issues: int):
    """Generar un archivo SQL de respaldo de la tabla sincronizada"""
    try:
        logger.info(f"Task {task_id}: === INICIANDO GENERACIÓN DE BACKUP ===")
        
        # Update task status
        background_tasks_store[task_id]["status"] = "generando_respaldo"
        background_tasks_store[task_id]["message"] = "Generando archivo de respaldo SQL..."
        background_tasks_store[task_id]["progress"] = 95  # Set progress to 95%
        
        # Obtener zona horaria de México
        mexico_tz = pytz.timezone('America/Mexico_City')
        mexico_time = datetime.now(mexico_tz)
        
        # Formato de fecha y hora para el nombre del archivo
        timestamp = mexico_time.strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"jira_sync_{timestamp}.sql"
        backup_path = BACKUPS_DIR / backup_filename
        
        logger.info(f"Task {task_id}: Generando backup en: {backup_path}")
        logger.info(f"Task {task_id}: Directorio de backups: {BACKUPS_DIR.absolute()}")
        
        # Ensure backups directory exists
        BACKUPS_DIR.mkdir(exist_ok=True)
        
        # Always use Python-based backup for reliability
        logger.info(f"Task {task_id}: Usando método Python para generar backup")
        
        # Generate backup using Python
        connection = mysql.connector.connect(
            host=config.mysql_host,
            port=config.mysql_port,
            user=config.mysql_user,
            password=config.mysql_password,
            database=config.mysql_database
        )
        
        cursor = connection.cursor()
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"-- Jira Sync Backup\n")
            f.write(f"-- Generated: {mexico_time.strftime('%Y-%m-%d %H:%M:%S')} (Mexico/Ciudad de México)\n")
            f.write(f"-- Task ID: {task_id}\n")
            f.write(f"-- Table: {table_name}\n")
            f.write(f"-- Total Issues: {total_issues}\n")
            f.write(f"-- Database: {config.mysql_database}\n")
            f.write(f"-- Host: {config.mysql_host}\n")
            f.write(f"-- ====================================\n\n")
            
            f.write(f"-- Backup Path: {backup_path.absolute()}\n")
            f.write(f"-- Container Path: /app/backups/{backup_filename}\n\n")
            
            f.write(f"USE `{config.mysql_database}`;\n\n")
            
            # Get CREATE TABLE statement
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
            create_result = cursor.fetchone()
            if create_result:
                create_table = create_result[1]
                f.write(f"-- Table structure for table `{table_name}`\n")
                f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                f.write(f"{create_table};\n\n")
                
                # Get all data
                cursor.execute(f"SELECT * FROM `{table_name}`")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                logger.info(f"Task {task_id}: Escribiendo {len(rows)} filas al backup")
                
                if rows:
                    f.write(f"-- Data for table `{table_name}`\n")
                    f.write(f"LOCK TABLES `{table_name}` WRITE;\n")
                    f.write(f"/*!40000 ALTER TABLE `{table_name}` DISABLE KEYS */;\n\n")
                    
                    # Write INSERT statements in batches
                    batch_size = 100
                    for batch_start in range(0, len(rows), batch_size):
                        batch_end = min(batch_start + batch_size, len(rows))
                        f.write(f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in columns])}) VALUES\n")
                        
                        for i in range(batch_start, batch_end):
                            row = rows[i]
                            values = []
                            for value in row:
                                if value is None:
                                    values.append("NULL")
                                elif isinstance(value, (int, float)):
                                    values.append(str(value))
                                elif isinstance(value, datetime):
                                    values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
                                elif isinstance(value, bytes):
                                    hex_value = value.hex()
                                    values.append(f"0x{hex_value}")
                                else:
                                    # Escape special characters
                                    escaped = str(value).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
                                    values.append(f"'{escaped}'")
                            
                            if i < batch_end - 1:
                                f.write(f"({', '.join(values)}),\n")
                            else:
                                f.write(f"({', '.join(values)});\n")
                        
                        f.write("\n")
                    
                    f.write(f"/*!40000 ALTER TABLE `{table_name}` ENABLE KEYS */;\n")
                    f.write("UNLOCK TABLES;\n")
                else:
                    f.write(f"-- No data found in table `{table_name}`\n")
            else:
                f.write(f"-- ERROR: Could not get table structure for `{table_name}`\n")
            
            f.write(f"\n-- End of backup\n")
            f.write(f"-- File size will be calculated after closing\n")
        
        cursor.close()
        connection.close()
        
        # Verify file was created
        if backup_path.exists():
            file_size = backup_path.stat().st_size
            logger.info(f"Task {task_id}: Backup generado exitosamente: {backup_filename} ({file_size} bytes)")
            logger.info(f"Task {task_id}: Ruta absoluta: {backup_path.absolute()}")
            
            # Update task with backup info
            background_tasks_store[task_id]["backup_file"] = backup_filename
            background_tasks_store[task_id]["backup_path"] = str(backup_path)
            background_tasks_store[task_id]["backup_absolute_path"] = str(backup_path.absolute())
            background_tasks_store[task_id]["backup_size"] = file_size
            
            return backup_filename
        else:
            logger.error(f"Task {task_id}: ERROR - El archivo de backup no se creó!")
            return None
    
    except Exception as e:
        logger.error(f"Task {task_id}: Error al generar backup: {str(e)}")
        logger.exception(e)  # Log full traceback
        background_tasks_store[task_id]["error"] = f"Error al generar backup: {str(e)}"
        return None


def get_field_type(value: Any) -> str:
    """Determine MySQL field type based on value"""
    if isinstance(value, bool):
        return "BOOLEAN"
    elif isinstance(value, int):
        return "BIGINT"
    elif isinstance(value, float):
        return "DOUBLE"
    elif isinstance(value, dict) or isinstance(value, list):
        return "JSON"
    else:
        # Default to TEXT for strings and unknown types
        return "TEXT"


def flatten_issue_fields(issue: Dict[str, Any], field_mapping: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Flatten nested issue fields for database storage with optional custom mapping"""
    flat_data = {"key": issue.get("key")}
    
    # Process standard fields
    for field_name, field_value in issue.get("fields", {}).items():
        # Determine the database column name
        if field_mapping and field_name in field_mapping:
            db_field_name = field_mapping[field_name]
        else:
            db_field_name = field_name
            
        if isinstance(field_value, dict):
            # Handle complex fields (like status, priority, etc.)
            if "name" in field_value:
                flat_data[f"{db_field_name}_name"] = field_value.get("name")
            if "value" in field_value:
                flat_data[f"{db_field_name}_value"] = field_value.get("value")
            # Store full JSON for complex objects
            flat_data[db_field_name] = json.dumps(field_value)
        elif isinstance(field_value, list):
            # Store lists as JSON
            flat_data[db_field_name] = json.dumps(field_value)
        else:
            flat_data[db_field_name] = field_value
    
    return flat_data


def ensure_table_exists(connection: mysql.connector.MySQLConnection, 
                       sync_request: JiraSyncRequest, 
                       issues: List[Dict[str, Any]]) -> None:
    """Ensure table exists with all necessary columns"""
    cursor = connection.cursor()
    
    # Extract field mapping if provided
    field_mapping = None
    if isinstance(sync_request.fields, dict):
        field_mapping = sync_request.fields
    
    # Get sample of fields from issues to determine structure
    all_fields = set()
    field_types = {}
    
    for issue in issues[:10]:  # Sample first 10 issues
        flat_issue = flatten_issue_fields(issue, field_mapping)
        for field_name, field_value in flat_issue.items():
            all_fields.add(field_name)
            if field_name not in field_types and field_value is not None:
                field_types[field_name] = get_field_type(field_value)
    
    # Create table if not exists
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {sync_request.mysql_table} (
        `key` VARCHAR(255) PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_table_sql)
    
    # Get existing columns
    cursor.execute(f"DESCRIBE {sync_request.mysql_table}")
    existing_columns = set(row[0] for row in cursor.fetchall())
    
    # Add missing columns
    for field_name in all_fields:
        if field_name not in existing_columns:
            field_type = field_types.get(field_name, "TEXT")
            alter_sql = f"ALTER TABLE {sync_request.mysql_table} ADD COLUMN `{field_name}` {field_type}"
            try:
                cursor.execute(alter_sql)
                logger.info(f"Added column: {field_name} ({field_type})")
            except Error as e:
                logger.warning(f"Could not add column {field_name}: {e}")
    
    connection.commit()
    cursor.close()


def sync_issues_to_database_with_progress(connection: mysql.connector.MySQLConnection,
                                        sync_request: JiraSyncRequest,
                                        issues: List[Dict[str, Any]],
                                        task_id: str) -> int:
    """Sync issues to database with progress tracking"""
    cursor = connection.cursor()
    synced_count = 0
    total_issues = len(issues)
    
    logger.info(f"Task {task_id}: Iniciando sincronización de {total_issues} issues")
    
    # Extract field mapping if provided
    field_mapping = None
    if isinstance(sync_request.fields, dict):
        field_mapping = sync_request.fields
    
    for index, issue in enumerate(issues):
        flat_issue = flatten_issue_fields(issue, field_mapping)
        
        # Build dynamic INSERT ... ON DUPLICATE KEY UPDATE query
        columns = list(flat_issue.keys())
        values = [flat_issue[col] for col in columns]
        
        # Create placeholders
        placeholders = ", ".join(["%s"] * len(columns))
        
        # Update columns for ON DUPLICATE KEY UPDATE
        update_clause = ", ".join([f"`{col}` = VALUES(`{col}`)" for col in columns if col != "key"])
        
        insert_sql = f"""
        INSERT INTO {sync_request.mysql_table} ({', '.join([f'`{col}`' for col in columns])})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE {update_clause}
        """
        
        try:
            cursor.execute(insert_sql, values)
            synced_count += 1
            
            # Update progress (50-100% range)
            if index % 10 == 0 or index == total_issues - 1:  # Update every 10 issues or on last
                progress = 50 + int((index + 1) / total_issues * 50)
                background_tasks_store[task_id].update({
                    "progress": progress,
                    "processed_issues": synced_count,
                    "message": f"Sincronizando: {synced_count}/{total_issues} issues"
                })
                
                if index % 50 == 0:  # Log every 50 issues
                    logger.info(f"Task {task_id}: Progreso {synced_count}/{total_issues} issues")
                
        except Error as e:
            logger.error(f"Error syncing issue {issue.get('key')}: {e}")
    
    connection.commit()
    cursor.close()
    
    logger.info(f"Task {task_id}: Sincronización completada - {synced_count}/{total_issues} issues")
    
    return synced_count


@app.get("/sync-status/{task_id}")
async def get_sync_status(task_id: str):
    """Get the status of a background sync task"""
    if task_id not in background_tasks_store:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_info = background_tasks_store[task_id]
    
    # Calculate percentage if in progress
    if task_info["status"] in ["descargando", "sincronizando"] and task_info["total_issues"] > 0:
        percentage = task_info["progress"]
    else:
        percentage = 0 if task_info["status"] not in ["completado"] else 100
    
    return {
        "task_id": task_id,
        "status": task_info["status"],
        "progress_percentage": percentage,
        "total_issues": task_info["total_issues"],
        "processed_issues": task_info["processed_issues"],
        "message": task_info["message"],
        "started_at": task_info["started_at"],
        "completed_at": task_info["completed_at"],
        "error": task_info["error"],
        "result": task_info.get("result")
    }


@app.get("/sync-tasks")
async def list_sync_tasks(limit: int = 10):
    """List recent sync tasks"""
    # Get tasks sorted by start time (most recent first)
    sorted_tasks = sorted(
        background_tasks_store.values(),
        key=lambda x: x["started_at"],
        reverse=True
    )[:limit]
    
    return {
        "tasks": sorted_tasks,
        "total": len(background_tasks_store)
    }


@app.delete("/sync-tasks/{task_id}")
async def delete_sync_task(task_id: str):
    """Delete a sync task and its associated backup file"""
    try:
        # Get task info
        if task_id not in background_tasks_store:
            # Check in database
            connection = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "localhost"),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", ""),
                database=os.getenv("MYSQL_DATABASE", "jiradb")
            )
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT backup_file FROM sync_logs WHERE task_id = %s
            """, (task_id,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Task not found")
            
            backup_file = result['backup_file']
            
            # Delete from database
            cursor.execute("DELETE FROM sync_logs WHERE task_id = %s", (task_id,))
            connection.commit()
            cursor.close()
            connection.close()
        else:
            # Get backup file from memory
            backup_file = background_tasks_store[task_id].get('backup_file')
            
            # Remove from memory
            del background_tasks_store[task_id]
        
        # Delete backup file if exists
        if backup_file:
            backup_path = BACKUPS_DIR / backup_file
            if backup_path.exists():
                backup_path.unlink()
                logger.info(f"Deleted backup file: {backup_file}")
        
        return {"message": f"Task {task_id} deleted successfully"}
    
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sync-logs/{task_id}")
async def get_sync_log_details(task_id: str):
    """Get detailed information about a specific sync task"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "jiradb")
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM sync_logs WHERE task_id = %s
        """, (task_id,))
        
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Parse JSON fields if they exist
        if result.get('config') and result['config']:
            try:
                result['config'] = json.loads(result['config'])
            except:
                result['config'] = None
                
        if result.get('result') and result['result']:
            try:
                result['result'] = json.loads(result['result'])
            except:
                result['result'] = None
        
        # Convert datetime to string
        if result.get('created_at'):
            result['created_at'] = result['created_at'].isoformat()
        if result.get('updated_at'):
            result['updated_at'] = result['updated_at'].isoformat()
        if result.get('started_at'):
            result['started_at'] = result['started_at'].isoformat()
        if result.get('completed_at'):
            result['completed_at'] = result['completed_at'].isoformat()
        
        return result
    
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error retrieving log details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sync-logs")
async def get_all_sync_logs(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get all sync logs with pagination"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "jiradb")
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Get total count
        cursor.execute("SELECT COUNT(*) as total FROM sync_logs")
        total = cursor.fetchone()['total']
        
        # Get logs with pagination - check which columns exist
        cursor.execute("SHOW COLUMNS FROM sync_logs")
        columns = [col[0] for col in cursor.fetchall()]
        
        # Build dynamic select based on available columns
        select_columns = ['task_id', 'status', 'total_issues', 'processed_issues', 
                         'created_at', 'backup_file', 'error_message']
        if 'updated_at' in columns:
            select_columns.insert(5, 'updated_at')
        if 'started_at' in columns:
            select_columns.insert(5, 'started_at')
        if 'completed_at' in columns:
            select_columns.insert(6, 'completed_at')
            
        columns_str = ', '.join(select_columns)
        
        cursor.execute(f"""
            SELECT {columns_str}
            FROM sync_logs 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        logs = cursor.fetchall()
        
        # Convert datetime to string
        for log in logs:
            if log.get('created_at'):
                log['created_at'] = log['created_at'].isoformat()
            if log.get('updated_at'):
                log['updated_at'] = log['updated_at'].isoformat()
            if log.get('started_at'):
                log['started_at'] = log['started_at'].isoformat()
            if log.get('completed_at'):
                log['completed_at'] = log['completed_at'].isoformat()
        
        cursor.close()
        connection.close()
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "logs": logs
        }
    
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/backups")
async def list_backups():
    """List all available backup files"""
    backups = []
    
    for backup_file in BACKUPS_DIR.glob("backup_*.sql"):
        stats = backup_file.stat()
        backups.append({
            "filename": backup_file.name,
            "size": stats.st_size,
            "created_at": datetime.fromtimestamp(stats.st_ctime).isoformat(),
            "task_id": backup_file.stem.split("_")[1]  # Extract task_id from filename
        })
    
    # Sort by creation date descending
    backups.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {
        "backups": backups,
        "total": len(backups)
    }


@app.get("/backups/{filename}")
async def download_backup(filename: str):
    """Download a specific backup file"""
    backup_path = BACKUPS_DIR / filename
    
    if not backup_path.exists() or not backup_path.is_file():
        raise HTTPException(status_code=404, detail="Backup file not found")
    
    return FileResponse(
        path=backup_path,
        filename=filename,
        media_type="application/sql",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.delete("/backups/{filename}")
async def delete_backup(filename: str):
    """Delete a specific backup file"""
    backup_path = BACKUPS_DIR / filename
    
    if not backup_path.exists() or not backup_path.is_file():
        raise HTTPException(status_code=404, detail="Backup file not found")
    
    try:
        backup_path.unlink()
        return {"message": f"Backup {filename} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting backup: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting backup: {str(e)}")


@app.post("/sync-logs")
async def get_sync_logs_from_db(connection_info: Dict[str, Any]):
    """Get sync logs from MySQL database"""
    try:
        # Create connection using provided info
        connection = mysql.connector.connect(
            host=connection_info["mysql_host"],
            port=connection_info.get("mysql_port", 3306),
            user=connection_info["mysql_user"],
            password=connection_info["mysql_password"],
            database=connection_info["mysql_database"]
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Get logs with pagination
        limit = connection_info.get("limit", 50)
        offset = connection_info.get("offset", 0)
        
        query = """
        SELECT * FROM sync_logs 
        ORDER BY started_at DESC 
        LIMIT %s OFFSET %s
        """
        
        cursor.execute(query, (limit, offset))
        logs = cursor.fetchall()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) as total FROM sync_logs")
        total = cursor.fetchone()["total"]
        
        cursor.close()
        connection.close()
        
        # Convert datetime objects to ISO format
        for log in logs:
            for key in ["started_at", "completed_at", "created_at"]:
                if key in log and log[key]:
                    log[key] = log[key].isoformat()
            # Parse JSON result if stored as string
            if log.get("result") and isinstance(log["result"], str):
                try:
                    log["result"] = json.loads(log["result"])
                except:
                    pass
        
        return {
            "logs": logs,
            "total": total,
            "limit": limit,
            "offset": offset
        }
        
    except Error as e:
        logger.error(f"Error getting logs from database: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Example usage endpoint to show request format
@app.get("/sync-example")
def get_sync_example():
    """Return an example of the sync request format"""
    return {
        "example_with_list": {
            "jira_domain": "your-domain.atlassian.net",
            "jira_email": "your-email@example.com",
            "jira_api_token": "your-api-token",
            "jql": "project = SAC",
            "fields": ["summary", "status", "priority", "assignee", "created", "updated"],
            "mysql_host": "localhost",
            "mysql_port": 3306,
            "mysql_user": "root",
            "mysql_password": "password",
            "mysql_database": "jiradb",
            "mysql_table": "jira_issues",
            "max_results_per_page": 50
        },
        "example_with_mapping": {
            "jira_domain": "your-domain.atlassian.net",
            "jira_email": "your-email@example.com",
            "jira_api_token": "your-api-token",
            "jql": "project = SAC",
            "fields": {
                "summary": "resumen",
                "status": "estado",
                "priority": "prioridad",
                "assignee": "asignado_a",
                "created": "fecha_creacion",
                "updated": "fecha_actualizacion",
                "customfield_10860": "tipo_cliente"
            },
            "mysql_host": "localhost",
            "mysql_port": 3306,
            "mysql_user": "root",
            "mysql_password": "password",
            "mysql_database": "jiradb",
            "mysql_table": "jira_issues",
            "max_results_per_page": 50
        }
    }


@app.post("/test-jira-connection")
async def test_jira_connection(jira_config: Dict[str, Any]):
    """
    Test Jira connection and JQL query without MySQL
    """
    try:
        # Handle both list and dict formats for fields
        if isinstance(jira_config.get("fields"), dict):
            fields = list(jira_config["fields"].keys())
        else:
            fields = jira_config.get("fields", ["summary", "status"])
            
        # Extract only Jira-related fields
        sync_request = JiraSyncRequest(
            jira_domain=jira_config["jira_domain"],
            jira_email=jira_config["jira_email"],
            jira_api_token=jira_config["jira_api_token"],
            jql=jira_config["jql"],
            fields=fields,  # Use the processed fields
            # Dummy MySQL config
            mysql_host="localhost",
            mysql_port=3306,
            mysql_user="root",
            mysql_password="",
            mysql_database="test",
            mysql_table="test"
        )
        
        # Get issue count
        issue_count = await get_issue_count(sync_request)
        
        # Fetch first page of issues
        url = f"https://{sync_request.jira_domain}/rest/api/3/search/jql"
        auth = HTTPBasicAuth(sync_request.jira_email, sync_request.jira_api_token)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "jql": sync_request.jql,
            "fields": fields,
            "maxResults": 5  # Just get first 5 for testing
        }
        
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        
        data = response.json()
        issues = data.get("issues", [])
        
        return {
            "success": True,
            "approximate_count": issue_count,
            "sample_issues": [
                {
                    "key": issue.get("key"),
                    "fields": issue.get("fields", {})
                } for issue in issues[:5]
            ],
            "message": f"Successfully connected to Jira. Found {issue_count} issues matching JQL."
        }
        
    except Exception as e:
        logger.error(f"Error testing Jira connection: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to connect to Jira. Please check your credentials and JQL."
        }


async def fetch_all_issues(sync_request: JiraSyncRequest, total_count: int) -> List[Dict[str, Any]]:
    """Fetch all issues using pagination (original function for compatibility)"""
    all_issues = []
    next_page_token = None
    
    url = f"https://{sync_request.jira_domain}/rest/api/3/search/jql"
    auth = HTTPBasicAuth(sync_request.jira_email, sync_request.jira_api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Extract field names for Jira API
    if isinstance(sync_request.fields, dict):
        jira_fields = list(sync_request.fields.keys())
    else:
        jira_fields = sync_request.fields
    
    while True:
        payload = {
            "jql": sync_request.jql,
            "fields": jira_fields,
            "maxResults": sync_request.max_results_per_page
        }
        
        if next_page_token:
            payload["nextPageToken"] = next_page_token
        
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        
        data = response.json()
        issues = data.get("issues", [])
        all_issues.extend(issues)
        
        logger.info(f"Fetched {len(all_issues)}/{total_count} issues")
        
        # Check if there are more pages
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break
    
    return all_issues


def sync_issues_to_database(connection: mysql.connector.MySQLConnection,
                           sync_request: JiraSyncRequest,
                           issues: List[Dict[str, Any]]) -> int:
    """Sync issues to database (original function for compatibility)"""
    cursor = connection.cursor()
    synced_count = 0
    
    # Extract field mapping if provided
    field_mapping = None
    if isinstance(sync_request.fields, dict):
        field_mapping = sync_request.fields
    
    for issue in issues:
        flat_issue = flatten_issue_fields(issue, field_mapping)
        
        # Build dynamic INSERT ... ON DUPLICATE KEY UPDATE query
        columns = list(flat_issue.keys())
        values = [flat_issue[col] for col in columns]
        
        # Create placeholders
        placeholders = ", ".join(["%s"] * len(columns))
        column_names = ", ".join([f"`{col}`" for col in columns])
        
        # Build update clause for ON DUPLICATE KEY UPDATE
        update_pairs = ", ".join([f"`{col}` = VALUES(`{col}`)" for col in columns if col != 'key'])
        
        insert_sql = f"""
        INSERT INTO {sync_request.mysql_table} ({column_names})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE {update_pairs}
        """
        
        try:
            cursor.execute(insert_sql, values)
            synced_count += 1
            
            if synced_count % 100 == 0:
                logger.info(f"Synced {synced_count} issues...")
                connection.commit()
        except Error as e:
            logger.error(f"Error syncing issue {flat_issue.get('key')}: {e}")
            # Continue with next issue
    
    connection.commit()
    cursor.close()
    
    return synced_count


@app.post("/sync-jira-issues-sync")
async def sync_jira_issues_synchronous(sync_request: JiraSyncRequest):
    """
    Synchronize Jira issues to MySQL database (synchronous version for backward compatibility)
    """
    try:
        # Step 1: Get approximate count of issues
        logger.info(f"Getting approximate count for JQL: {sync_request.jql}")
        issue_count = await get_issue_count(sync_request)
        logger.info(f"Found approximately {issue_count} issues")
        
        # Step 2: Connect to MySQL
        connection = connect_to_mysql(sync_request)
        
        # Step 3: Fetch all issues with pagination
        logger.info("Fetching all issues...")
        all_issues = await fetch_all_issues(sync_request, issue_count)
        logger.info(f"Fetched {len(all_issues)} issues")
        
        # Step 4: Ensure table exists and has all necessary columns
        ensure_table_exists(connection, sync_request, all_issues)
        
        # Step 5: Sync issues to database
        synced_count = sync_issues_to_database(connection, sync_request, all_issues)
        
        # Close connection
        connection.close()
        
        return {
            "success": True,
            "message": f"Successfully synced {synced_count} issues",
            "total_issues": len(all_issues),
            "approximate_count": issue_count
        }
        
    except Exception as e:
        logger.error(f"Error during sync: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/test-mysql-connection")
async def test_mysql_connection(config: JiraSyncRequest):
    """Test MySQL connection with provided credentials"""
    try:
        connection = mysql.connector.connect(
            host=config.mysql_host,
            port=config.mysql_port,
            user=config.mysql_user,
            password=config.mysql_password,
            database=config.mysql_database
        )
        
        # Test query
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        connection.close()
        
        return {"success": True, "message": "Conexión exitosa a MySQL"}
    
    except mysql.connector.Error as e:
        logger.error(f"MySQL connection test failed: {e}")
        raise HTTPException(status_code=400, detail=f"Error de conexión MySQL: {str(e)}")
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Error al probar conexión: {str(e)}")


@app.get("/backups/{filename}/info")
async def get_backup_info(filename: str):
    """Get detailed information about a backup file"""
    backup_path = BACKUPS_DIR / filename
    
    if not backup_path.exists():
        raise HTTPException(status_code=404, detail="Backup file not found")
    
    try:
        stat = backup_path.stat()
        
        # Get absolute path
        absolute_path = str(backup_path.absolute())
        
        return {
            "filename": filename,
            "path": str(backup_path),
            "absolute_path": absolute_path,
            "container_path": f"/app/backups/{filename}",  # Path inside Docker container
            "size": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "download_url": f"/backups/{filename}",
            "exists": True
        }
    except Exception as e:
        logger.error(f"Error getting backup info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sync-logs/load-from-db/{task_id}")
async def load_sync_log_from_db(task_id: str):
    """Load sync log directly from database"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "jiradb")
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Get log with configuration
        cursor.execute("""
            SELECT 
                sl.*,
                JSON_UNQUOTE(JSON_EXTRACT(sl.result, '$.backup_file')) as backup_filename,
                JSON_UNQUOTE(JSON_EXTRACT(sl.result, '$.backup_url')) as backup_url
            FROM sync_logs sl
            WHERE sl.task_id = %s
        """, (task_id,))
        
        result = cursor.fetchone()
        
        if not result:
            # Check in memory
            if task_id in background_tasks_store:
                return background_tasks_store[task_id]
            raise HTTPException(status_code=404, detail="Sync log not found")
        
        # Parse JSON fields
        if result['result']:
            result['result'] = json.loads(result['result'])
        
        # Convert datetime to string
        for field in ['started_at', 'completed_at', 'created_at']:
            if result.get(field):
                result[field] = result[field].isoformat()
        
        # Add backup info if exists
        if result.get('backup_filename'):
            backup_path = BACKUPS_DIR / result['backup_filename']
            result['backup_exists'] = backup_path.exists()
            result['backup_absolute_path'] = str(backup_path.absolute()) if backup_path.exists() else None
        
        cursor.close()
        connection.close()
        
        return result
        
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error loading sync log: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/export-table")
async def export_table(export_request: Dict[str, Any]):
    """Export any MySQL table as SQL file"""
    try:
        # Extract parameters
        mysql_config = {
            "host": export_request.get("mysql_host", "localhost"),
            "port": export_request.get("mysql_port", 3306),
            "user": export_request.get("mysql_user", "root"),
            "password": export_request.get("mysql_password", ""),
            "database": export_request.get("mysql_database", "jiradb")
        }
        table_name = export_request.get("table_name")
        
        if not table_name:
            raise HTTPException(status_code=400, detail="table_name is required")
        
        # Connect to MySQL
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()
        
        # Get Mexico timezone
        mexico_tz = pytz.timezone('America/Mexico_City')
        mexico_time = datetime.now(mexico_tz)
        timestamp = mexico_time.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Generate filename
        filename = f"{table_name}_export_{timestamp}.sql"
        filepath = BACKUPS_DIR / filename
        
        # Get table structure
        cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
        create_table_result = cursor.fetchone()
        if not create_table_result:
            raise HTTPException(status_code=404, detail=f"Table {table_name} not found")
        
        create_table_sql = create_table_result[1]
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        row_count = cursor.fetchone()[0]
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"-- Table Export\n")
            f.write(f"-- Generated: {mexico_time.strftime('%Y-%m-%d %H:%M:%S')} (Mexico/Ciudad de México)\n")
            f.write(f"-- Database: {mysql_config['database']}\n")
            f.write(f"-- Table: {table_name}\n")
            f.write(f"-- Total Rows: {row_count}\n")
            f.write(f"-- Generated by Jira Sync Manager\n\n")
            
            f.write("SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';\n")
            f.write("START TRANSACTION;\n")
            f.write("SET time_zone = '+00:00';\n\n")
            
            # Write table structure
            f.write(f"-- Table structure for table `{table_name}`\n")
            f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
            f.write(f"{create_table_sql};\n\n")
            
            # Export data
            if row_count > 0:
                f.write(f"-- Dumping data for table `{table_name}`\n\n")
                
                # Get column names
                cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
                columns = [col[0] for col in cursor.fetchall()]
                column_names = ", ".join([f"`{col}`" for col in columns])
                
                # Fetch and write data in batches
                batch_size = 1000
                offset = 0
                
                while offset < row_count:
                    cursor.execute(f"SELECT * FROM `{table_name}` LIMIT {batch_size} OFFSET {offset}")
                    rows = cursor.fetchall()
                    
                    if rows:
                        values_list = []
                        for row in rows:
                            values = []
                            for value in row:
                                if value is None:
                                    values.append("NULL")
                                elif isinstance(value, (int, float)):
                                    values.append(str(value))
                                elif isinstance(value, datetime):
                                    values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
                                elif isinstance(value, bytes):
                                    # Handle binary data
                                    hex_string = value.hex()
                                    values.append(f"0x{hex_string}")
                                else:
                                    # Escape single quotes and backslashes
                                    escaped_value = str(value).replace('\\', '\\\\').replace("'", "\\'")
                                    values.append(f"'{escaped_value}'")
                            values_list.append(f"({', '.join(values)})")
                        
                        # Write INSERT statement
                        f.write(f"INSERT INTO `{table_name}` ({column_names}) VALUES\n")
                        f.write(",\n".join(values_list))
                        f.write(";\n\n")
                    
                    offset += batch_size
                    logger.info(f"Exported {min(offset, row_count)}/{row_count} rows from {table_name}")
            
            f.write("COMMIT;\n")
        
        # Get file info
        file_stat = filepath.stat()
        file_size = file_stat.st_size
        
        cursor.close()
        connection.close()
        
        return {
            "success": True,
            "filename": filename,
            "filepath": str(filepath),
            "download_url": f"/backups/{filename}",
            "table_name": table_name,
            "row_count": row_count,
            "file_size": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
            "generated_at": mexico_time.isoformat()
        }
        
    except mysql.connector.Error as e:
        logger.error(f"MySQL error during table export: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error exporting table: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/logs/by-task")
async def get_logs_by_task_id(request: Dict[str, Any]):
    """
    Get logs for a specific task_id
    
    Request body:
    {
        "task_id": "string"
    }
    """
    try:
        # Validar que se proporcione task_id
        task_id = request.get("task_id")
        if not task_id:
            raise HTTPException(status_code=400, detail="task_id is required")
        
        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "jiradb")
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Primero verificar si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'sync_logs'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            cursor.close()
            connection.close()
            return {
                "error": "Table sync_logs does not exist",
                "task_id": task_id,
                "logs": []
            }
        
        # Obtener las columnas de la tabla
        cursor.execute("DESCRIBE sync_logs")
        columns = [row['Field'] for row in cursor.fetchall()]
        logger.info(f"Available columns in sync_logs: {columns}")
        
        # Consultar los logs para el task_id específico
        query = """
        SELECT * FROM sync_logs 
        WHERE task_id = %s
        ORDER BY created_at DESC
        """
        
        cursor.execute(query, (task_id,))
        logs = cursor.fetchall()
        
        # Convertir datetime a string
        for log in logs:
            for key, value in log.items():
                if isinstance(value, datetime):
                    log[key] = value.isoformat()
                elif isinstance(value, bytes):
                    # Intentar decodificar bytes como JSON
                    try:
                        log[key] = json.loads(value.decode('utf-8'))
                    except:
                        log[key] = value.decode('utf-8', errors='ignore')
        
        cursor.close()
        connection.close()
        
        return {
            "task_id": task_id,
            "total_logs": len(logs),
            "logs": logs,
            "available_columns": columns
        }
        
    except mysql.connector.Error as e:
        logger.error(f"Database error in get_logs_by_task_id: {e}")
        return {
            "error": f"Database error: {str(e)}",
            "task_id": task_id,
            "logs": []
        }
    except Exception as e:
        logger.error(f"Unexpected error in get_logs_by_task_id: {e}")
        logger.exception(e)
        return {
            "error": f"Unexpected error: {str(e)}",
            "task_id": task_id,
            "logs": []
        }


@app.post("/api/logs/test-connection")
async def test_logs_connection():
    """Test connection to sync_logs table and show its structure"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "jiradb")
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'sync_logs'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            # Create the table
            ensure_logs_table_exists(connection)
            return {
                "status": "Table created",
                "message": "sync_logs table was created successfully"
            }
        
        # Get table structure
        cursor.execute("DESCRIBE sync_logs")
        structure = cursor.fetchall()
        
        # Get row count
        cursor.execute("SELECT COUNT(*) as count FROM sync_logs")
        count = cursor.fetchone()['count']
        
        # Get sample data
        cursor.execute("SELECT * FROM sync_logs ORDER BY created_at DESC LIMIT 5")
        sample_data = cursor.fetchall()
        
        # Convert datetime to string
        for row in sample_data:
            for key, value in row.items():
                if isinstance(value, datetime):
                    row[key] = value.isoformat()
                elif isinstance(value, bytes):
                    try:
                        row[key] = json.loads(value.decode('utf-8'))
                    except:
                        row[key] = value.decode('utf-8', errors='ignore')
        
        cursor.close()
        connection.close()
        
        return {
            "status": "Connected",
            "table_exists": True,
            "row_count": count,
            "table_structure": structure,
            "sample_data": sample_data
        }
        
    except Exception as e:
        logger.error(f"Error testing logs connection: {e}")
        return {
            "status": "Error",
            "error": str(e),
            "table_exists": False
        }


@app.get("/api/backups/verify")
async def verify_backups():
    """Verify backup files existence and get full server paths"""
    try:
        # Get absolute path of backups directory
        backups_abs_path = BACKUPS_DIR.resolve()
        
        backups_info = {
            "backups_directory": str(backups_abs_path),
            "directory_exists": BACKUPS_DIR.exists(),
            "is_directory": BACKUPS_DIR.is_dir(),
            "backups": [],
            "debug_info": {
                "cwd": str(Path.cwd()),
                "backups_dir_relative": str(BACKUPS_DIR),
                "all_files_in_dir": []
            }
        }
        
        if not BACKUPS_DIR.exists():
            BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
            backups_info["message"] = "Backups directory was created"
        
        # Debug: List ALL files in the directory
        if BACKUPS_DIR.exists() and BACKUPS_DIR.is_dir():
            try:
                all_files = list(BACKUPS_DIR.iterdir())
                backups_info["debug_info"]["all_files_in_dir"] = [f.name for f in all_files]
                backups_info["debug_info"]["total_files_found"] = len(all_files)
            except Exception as e:
                backups_info["debug_info"]["error_listing_files"] = str(e)
        
        # List all SQL files in the directory - try different patterns
        sql_files = []
        
        # Method 1: Using glob with *.sql
        try:
            sql_files = list(BACKUPS_DIR.glob("*.sql"))
            backups_info["debug_info"]["glob_sql_count"] = len(sql_files)
        except Exception as e:
            backups_info["debug_info"]["glob_error"] = str(e)
        
        # Method 2: If no files found, try iterdir with manual filter
        if not sql_files and BACKUPS_DIR.exists():
            try:
                for item in BACKUPS_DIR.iterdir():
                    if item.is_file() and item.suffix.lower() == '.sql':
                        sql_files.append(item)
                backups_info["debug_info"]["iterdir_sql_count"] = len(sql_files)
            except Exception as e:
                backups_info["debug_info"]["iterdir_error"] = str(e)
        
        # Process SQL files found
        for backup_file in sql_files:
            try:
                stats = backup_file.stat()
                file_info = {
                    "filename": backup_file.name,
                    "full_path": str(backup_file.resolve()),
                    "relative_path": str(backup_file.relative_to(Path.cwd())),
                    "size_bytes": stats.st_size,
                    "size_mb": round(stats.st_size / (1024 * 1024), 2),
                    "created_at": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                    "modified_at": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    "is_file": backup_file.is_file(),
                    "exists": backup_file.exists(),
                    "readable": os.access(str(backup_file), os.R_OK),
                    "writable": os.access(str(backup_file), os.W_OK)
                }
                backups_info["backups"].append(file_info)
            except Exception as e:
                logger.error(f"Error processing backup file {backup_file}: {e}")
        
        # Sort by creation date descending
        backups_info["backups"].sort(key=lambda x: x["created_at"], reverse=True)
        
        # Add summary
        backups_info["summary"] = {
            "total_backups": len(backups_info["backups"]),
            "total_size_mb": round(sum(b["size_mb"] for b in backups_info["backups"]), 2),
            "working_directory": str(Path.cwd()),
            "python_version": sys.version,
            "platform": sys.platform
        }
        
        return backups_info
        
    except Exception as e:
        logger.error(f"Error verifying backups: {e}")
        return {
            "error": str(e),
            "backups_directory": str(BACKUPS_DIR),
            "working_directory": str(Path.cwd())
        }


@app.get("/api/backups/check/{filename}")
async def check_backup_file(filename: str):
    """Check if a specific backup file exists and get detailed info"""
    try:
        backup_path = BACKUPS_DIR / filename
        
        if not backup_path.exists():
            return {
                "exists": False,
                "filename": filename,
                "searched_path": str(backup_path.resolve()),
                "backups_directory": str(BACKUPS_DIR.resolve())
            }
        
        stats = backup_path.stat()
        
        # Read first few lines to verify it's a valid SQL file
        preview_lines = []
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i < 10:  # First 10 lines
                        preview_lines.append(line.strip())
                    else:
                        break
        except Exception as e:
            preview_lines = [f"Error reading file: {str(e)}"]
        
        return {
            "exists": True,
            "filename": filename,
            "full_path": str(backup_path.resolve()),
            "relative_path": str(backup_path.relative_to(Path.cwd())),
            "size_bytes": stats.st_size,
            "size_mb": round(stats.st_size / (1024 * 1024), 2),
            "created_at": datetime.fromtimestamp(stats.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stats.st_mtime).isoformat(),
            "is_file": backup_path.is_file(),
            "readable": os.access(str(backup_path), os.R_OK),
            "writable": os.access(str(backup_path), os.W_OK),
            "preview": preview_lines,
            "download_url": f"/backups/{filename}"
        }
        
    except Exception as e:
        logger.error(f"Error checking backup file: {e}")
        return {
            "error": str(e),
            "filename": filename,
            "backups_directory": str(BACKUPS_DIR.resolve())
        }


@app.post("/api/backups/create-test")
async def create_test_backup():
    """Create a test backup file to verify the backup system is working"""
    try:
        # Ensure backups directory exists
        BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create test backup filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        test_filename = f"test_backup_{timestamp}.sql"
        test_filepath = BACKUPS_DIR / test_filename
        
        # Write test content
        test_content = f"""-- Test Backup File
-- Created: {datetime.now().isoformat()}
-- Purpose: Verify backup system functionality

CREATE TABLE IF NOT EXISTS test_table (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    created_at TIMESTAMP
);

INSERT INTO test_table VALUES 
    (1, 'Test Record 1', NOW()),
    (2, 'Test Record 2', NOW()),
    (3, 'Test Record 3', NOW());

-- End of test backup
"""
        
        with open(test_filepath, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Verify file was created
        if test_filepath.exists():
            stats = test_filepath.stat()
            return {
                "success": True,
                "message": "Test backup created successfully",
                "filename": test_filename,
                "full_path": str(test_filepath.resolve()),
                "size_bytes": stats.st_size,
                "content_preview": test_content.split('\n')[:5]
            }
        else:
            return {
                "success": False,
                "message": "Failed to create test backup",
                "attempted_path": str(test_filepath)
            }
            
    except Exception as e:
        logger.error(f"Error creating test backup: {e}")
        return {
            "success": False,
            "error": str(e),
            "backups_directory": str(BACKUPS_DIR.resolve())
        }


@app.post("/api/logs/reset-table")
async def reset_logs_table():
    """Reset the sync_logs table - delete all records and associated backup files"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "jiradb")
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # First, get all backup files to delete
        cursor.execute("SELECT backup_file FROM sync_logs WHERE backup_file IS NOT NULL")
        backup_files = cursor.fetchall()
        
        # Delete all records from sync_logs
        cursor.execute("TRUNCATE TABLE sync_logs")
        connection.commit()
        
        # Delete physical backup files
        deleted_files = []
        failed_files = []
        
        for row in backup_files:
            backup_file = row['backup_file']
            if backup_file:
                backup_path = BACKUPS_DIR / backup_file
                try:
                    if backup_path.exists():
                        backup_path.unlink()
                        deleted_files.append(backup_file)
                        logger.info(f"Deleted backup file: {backup_file}")
                    else:
                        logger.warning(f"Backup file not found: {backup_file}")
                except Exception as e:
                    logger.error(f"Error deleting backup file {backup_file}: {e}")
                    failed_files.append(backup_file)
        
        cursor.close()
        connection.close()
        
        return {
            "success": True,
            "message": "Tabla de logs reseteada exitosamente",
            "deleted_files": len(deleted_files),
            "failed_files": len(failed_files),
            "details": {
                "deleted": deleted_files,
                "failed": failed_files
            }
        }
        
    except mysql.connector.Error as e:
        logger.error(f"Database error in reset_logs_table: {e}")
        return {
            "success": False,
            "error": f"Error de base de datos: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Error resetting logs table: {e}")
        return {
            "success": False,
            "error": f"Error inesperado: {str(e)}"
        }


@app.delete("/api/logs/{task_id}")
async def delete_single_log(task_id: str):
    """Delete a single log record and its associated backup file"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "jiradb")
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # First, get the backup file name
        cursor.execute("SELECT backup_file FROM sync_logs WHERE task_id = %s", (task_id,))
        result = cursor.fetchone()
        
        if not result:
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail="Log not found")
        
        backup_file = result.get('backup_file')
        
        # Delete the log record
        cursor.execute("DELETE FROM sync_logs WHERE task_id = %s", (task_id,))
        connection.commit()
        
        # Delete the physical backup file if exists
        file_deleted = False
        if backup_file:
            backup_path = BACKUPS_DIR / backup_file
            try:
                if backup_path.exists():
                    backup_path.unlink()
                    file_deleted = True
                    logger.info(f"Deleted backup file: {backup_file}")
            except Exception as e:
                logger.error(f"Error deleting backup file {backup_file}: {e}")
        
        # Also remove from memory if exists
        if task_id in background_tasks_store:
            del background_tasks_store[task_id]
        
        cursor.close()
        connection.close()
        
        return {
            "success": True,
            "message": f"Log {task_id} eliminado exitosamente",
            "backup_file_deleted": file_deleted,
            "backup_file": backup_file
        }
        
    except HTTPException:
        raise
    except mysql.connector.Error as e:
        logger.error(f"Database error deleting log: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error deleting log: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


@app.get("/api/logs/all")
async def get_all_logs_simple():
    """Get all logs in a simple format for the logs viewer"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "jiradb")
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Get all logs ordered by creation date
        cursor.execute("""
            SELECT task_id, status, total_issues, processed_issues, 
                   created_at, backup_file, error_message, jql_query
            FROM sync_logs 
            ORDER BY created_at DESC
        """)
        
        logs = cursor.fetchall()
        
        # Convert datetime to string and parse result JSON
        for log in logs:
            if log.get('created_at'):
                log['created_at'] = log['created_at'].isoformat()
        
        cursor.close()
        connection.close()
        
        return {
            "success": True,
            "logs": logs,
            "total": len(logs)
        }
        
    except mysql.connector.Error as e:
        logger.error(f"Database error getting all logs: {e}")
        return {
            "success": False,
            "error": f"Error de base de datos: {str(e)}",
            "logs": []
        }
    except Exception as e:
        logger.error(f"Error getting all logs: {e}")
        return {
            "success": False,
            "error": f"Error inesperado: {str(e)}",
            "logs": []
        } 