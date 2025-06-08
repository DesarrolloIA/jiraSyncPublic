<template>
  <div class="space-y-8">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">🔧 Backend Development Masterclass</h2>
    
    <!-- Introducción -->
    <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-6 mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-3">🐍 Python FastAPI Backend - Guía Completa</h3>
      <p class="text-gray-700 mb-4">
        Esta masterclass te llevará desde cero hasta experto en el backend de Jira-MySQL Sync. 
        Aprenderás a manejar APIs REST asíncronas, conexiones a bases de datos, y procesamiento en background.
        Al finalizar serás capaz de:
      </p>
      <ul class="list-disc list-inside space-y-1 text-gray-700">
        <li>Construir APIs REST escalables con FastAPI</li>
        <li>Manejar operaciones asíncronas y background tasks</li>
        <li>Integrar APIs externas (Jira) con tu sistema</li>
        <li>Implementar patrones de diseño profesionales</li>
        <li>Extender el backend con nuevas funcionalidades</li>
      </ul>
    </div>

    <!-- Arquitectura del Backend -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🏗️ Arquitectura del Backend</h3>
      
      <div class="bg-gray-50 rounded-lg p-6 mb-4">
        <h4 class="font-semibold text-gray-900 mb-3">Stack Tecnológico Backend</h4>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white rounded p-4 border border-gray-200">
            <h5 class="font-semibold text-green-600 mb-2">Framework Core</h5>
            <ul class="text-sm space-y-1">
              <li>🚀 FastAPI 0.104+</li>
              <li>🐍 Python 3.8+</li>
              <li>⚡ Uvicorn (ASGI server)</li>
              <li>📝 Pydantic (Data validation)</li>
            </ul>
          </div>
          <div class="bg-white rounded p-4 border border-gray-200">
            <h5 class="font-semibold text-blue-600 mb-2">Base de Datos</h5>
            <ul class="text-sm space-y-1">
              <li>🗄️ MySQL 8.0+</li>
              <li>🔌 mysql-connector-python</li>
              <li>🔄 Connection pooling</li>
              <li>📊 Dynamic table creation</li>
            </ul>
          </div>
          <div class="bg-white rounded p-4 border border-gray-200">
            <h5 class="font-semibold text-purple-600 mb-2">Integraciones</h5>
            <ul class="text-sm space-y-1">
              <li>🎯 Jira Cloud REST API</li>
              <li>🔐 Basic Auth (API tokens)</li>
              <li>📥 Requests library</li>
              <li>🧵 Threading para tasks</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="bg-gray-50 rounded-lg p-6">
        <h4 class="font-semibold text-gray-900 mb-3">Estructura del Proyecto Backend</h4>
        <pre class="text-sm bg-gray-900 text-gray-100 p-4 rounded overflow-x-auto"><code>my-fastapi-app/
├── main.py                 # Aplicación principal con todos los endpoints
├── requirements.txt        # Dependencias Python
├── .env                    # Variables de entorno (no versionado)
├── Dockerfile             # Configuración Docker
├── .dockerignore          # Archivos a ignorar en Docker
├── backups/               # Directorio de respaldos SQL generados
│   └── *.sql             # Archivos de respaldo
├── postman_examples/      # Ejemplos para testing
│   ├── README.md
│   └── *.json           # Colecciones Postman
└── README.md             # Documentación del proyecto</code></pre>
      </div>
    </div>

    <!-- FastAPI Fundamentals -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🎓 FastAPI Fundamentals</h3>
      
      <div class="space-y-6">
        <!-- Creación de la App -->
        <div class="border rounded-lg p-6">
          <h4 class="font-semibold text-gray-900 mb-3">1. Creación y Configuración de la App</h4>
          
          <div class="bg-gray-50 rounded p-4 mb-3">
            <p class="text-sm font-semibold mb-2">Configuración Inicial:</p>
            <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

# Crear instancia de FastAPI
app = FastAPI(
    title="Jira MySQL Sync API",
    description="API para sincronizar issues de Jira con MySQL",
    version="2.0.0"
)

# Configurar CORS para permitir requests del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Jira MySQL Sync API",
        "version": "2.0.0",
        "status": "running"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)</code></pre>
          </div>

          <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4">
            <p class="text-sm text-yellow-700">
              <strong>💡 Concepto Clave:</strong> FastAPI automáticamente genera documentación interactiva 
              en <code>/docs</code> (Swagger UI) y <code>/redoc</code> (ReDoc).
            </p>
          </div>
        </div>

        <!-- Modelos Pydantic -->
        <div class="border rounded-lg p-6">
          <h4 class="font-semibold text-gray-900 mb-3">2. Modelos Pydantic - Validación de Datos</h4>
          
          <div class="bg-gray-50 rounded p-4 mb-3">
            <p class="text-sm font-semibold mb-2">Definición de Modelos:</p>
            <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>from pydantic import BaseModel, Field, validator
from typing import Dict, Optional, List
from datetime import datetime

# Configuración de Jira
class JiraConfig(BaseModel):
    jira_domain: str = Field(..., example="lla.atlassian.net")
    jira_email: str = Field(..., example="user@example.com")
    jira_api_token: str = Field(..., min_length=10)
    jql: str = Field(..., example="project = SAC AND updated >= -7d")
    fields: Dict[str, str] = Field(default_factory=lambda: {
        "summary": "resumen",
        "status": "estado",
        "description": "descripcion"
    })
    max_results_per_page: int = Field(default=50, ge=1, le=100)
    
    @validator('jira_email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido')
        return v
    
    @validator('jira_domain')
    def validate_domain(cls, v):
        if not v.endswith('.atlassian.net'):
            raise ValueError('Dominio debe terminar en .atlassian.net')
        return v

# Configuración de MySQL
class MySQLConfig(BaseModel):
    mysql_host: str = Field(default="localhost")
    mysql_port: int = Field(default=3306, ge=1, le=65535)
    mysql_user: str = Field(..., example="root")
    mysql_password: str
    mysql_database: str = Field(..., example="jiradb")
    mysql_table: str = Field(default="jira_issues")
    
    class Config:
        schema_extra = {
            "example": {
                "mysql_host": "localhost",
                "mysql_port": 3306,
                "mysql_user": "root",
                "mysql_password": "password123",
                "mysql_database": "jiradb",
                "mysql_table": "jira_issues"
            }
        }

# Request completo de sincronización
class SyncRequest(BaseModel):
    # Heredar campos de ambas configuraciones
    jira_domain: str
    jira_email: str
    jira_api_token: str
    jql: str
    fields: Dict[str, str]
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_database: str
    mysql_table: str
    max_results_per_page: int = 50</code></pre>
          </div>

          <div class="bg-blue-50 rounded p-4">
            <p class="text-sm font-semibold text-blue-700 mb-2">🎯 Ventajas de Pydantic:</p>
            <ul class="text-sm space-y-1 list-disc list-inside">
              <li>Validación automática de tipos y valores</li>
              <li>Documentación automática en OpenAPI</li>
              <li>Serialización/deserialización JSON integrada</li>
              <li>Mensajes de error claros y descriptivos</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Sistema de Background Tasks -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">⚡ Sistema de Background Tasks</h3>
      
      <div class="border rounded-lg p-6">
        <h4 class="font-semibold text-gray-900 mb-3">Implementación de Tareas Asíncronas</h4>
        
        <div class="bg-gray-50 rounded p-4 mb-3">
          <p class="text-sm font-semibold mb-2">Sistema de Tasks con Threading:</p>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>import threading
import uuid
from datetime import datetime
from typing import Dict, Optional

# Store global para tareas
tasks_store: Dict[str, Dict] = {}

# Modelo de estado de tarea
class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress_percentage: int = 0
    total_issues: int = 0
    processed_issues: int = 0
    message: str = ""
    started_at: str
    completed_at: Optional[str] = None
    error: Optional[str] = None
    result: Optional[Dict] = None
    backup_file: Optional[str] = None

def update_task_status(
    task_id: str,
    status: str,
    progress_percentage: int = None,
    total_issues: int = None,
    processed_issues: int = None,
    message: str = None,
    error: str = None,
    result: dict = None,
    backup_file: str = None
):
    """Actualiza el estado de una tarea en el store global"""
    if task_id in tasks_store:
        task = tasks_store[task_id]
        task['status'] = status
        
        if progress_percentage is not None:
            task['progress_percentage'] = progress_percentage
        if total_issues is not None:
            task['total_issues'] = total_issues
        if processed_issues is not None:
            task['processed_issues'] = processed_issues
        if message is not None:
            task['message'] = message
        if error is not None:
            task['error'] = error
        if result is not None:
            task['result'] = result
        if backup_file is not None:
            task['backup_file'] = backup_file
            
        if status in ['completado', 'error']:
            task['completed_at'] = datetime.now().isoformat()

# Endpoint principal de sincronización
@app.post("/sync-jira-issues", response_model=Dict[str, str])
async def sync_jira_issues(request: SyncRequest):
    # Generar ID único para la tarea
    task_id = str(uuid.uuid4())
    
    # Inicializar tarea en el store
    tasks_store[task_id] = {
        'task_id': task_id,
        'status': 'iniciando',
        'progress_percentage': 0,
        'total_issues': 0,
        'processed_issues': 0,
        'message': 'Iniciando sincronización...',
        'started_at': datetime.now().isoformat(),
        'completed_at': None,
        'error': None,
        'result': None,
        'backup_file': None
    }
    
    # Ejecutar sincronización en background
    thread = threading.Thread(
        target=sync_jira_to_mysql_background,
        args=(task_id, request.dict())
    )
    thread.daemon = True
    thread.start()
    
    return {"task_id": task_id, "status": "started"}

# Endpoint para consultar estado
@app.get("/sync-status/{task_id}", response_model=TaskStatus)
async def get_sync_status(task_id: str):
    if task_id not in tasks_store:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskStatus(**tasks_store[task_id])</code></pre>
        </div>

        <div class="bg-purple-50 rounded p-4">
          <p class="text-sm font-semibold text-purple-700 mb-2">🔄 Flujo de Trabajo Asíncrono:</p>
          <ol class="text-sm space-y-1 list-decimal list-inside">
            <li>Cliente envía request de sincronización</li>
            <li>API crea task_id y retorna inmediatamente</li>
            <li>Proceso se ejecuta en background thread</li>
            <li>Cliente hace polling del estado con task_id</li>
            <li>Cuando termina, cliente obtiene resultados</li>
          </ol>
        </div>
      </div>
    </div>

    <!-- Integración con Jira -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🎯 Integración con Jira Cloud API</h3>
      
      <div class="border rounded-lg p-6">
        <h4 class="font-semibold text-gray-900 mb-3">Implementación del Cliente Jira</h4>
        
        <div class="bg-gray-50 rounded p-4 mb-3">
          <p class="text-sm font-semibold mb-2">Función para Obtener Issues:</p>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>import requests
from requests.auth import HTTPBasicAuth
import base64

def get_jira_issues(config: dict, task_id: str) -> list:
    """Obtiene issues de Jira usando JQL con paginación"""
    
    # Configurar autenticación
    auth = HTTPBasicAuth(config['jira_email'], config['jira_api_token'])
    base_url = f"https://{config['jira_domain']}/rest/api/3/search"
    
    # Parámetros de búsqueda
    params = {
        'jql': config['jql'],
        'maxResults': config['max_results_per_page'],
        'startAt': 0,
        'fields': ','.join(config['fields'].keys())
    }
    
    all_issues = []
    total_issues = 0
    
    try:
        # Primera llamada para obtener el total
        update_task_status(task_id, 'obteniendo_total', message='Consultando total de issues...')
        
        response = requests.get(base_url, params=params, auth=auth)
        response.raise_for_status()
        
        data = response.json()
        total_issues = data['total']
        
        update_task_status(
            task_id, 
            'descargando',
            total_issues=total_issues,
            message=f'Total de issues encontrados: {total_issues}'
        )
        
        # Descargar todos los issues con paginación
        while True:
            response = requests.get(base_url, params=params, auth=auth)
            response.raise_for_status()
            
            data = response.json()
            issues = data['issues']
            all_issues.extend(issues)
            
            # Actualizar progreso
            progress = int((len(all_issues) / total_issues) * 50)  # 50% para descarga
            update_task_status(
                task_id,
                'descargando',
                progress_percentage=progress,
                processed_issues=len(all_issues),
                message=f'Descargando issues: {len(all_issues)}/{total_issues}'
            )
            
            # Verificar si hay más páginas
            if len(all_issues) >= total_issues:
                break
                
            params['startAt'] += params['maxResults']
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Error al conectar con Jira: {str(e)}"
        update_task_status(task_id, 'error', error=error_msg)
        raise Exception(error_msg)
    
    return all_issues

# Función auxiliar para procesar campos de Jira
def extract_field_value(issue: dict, field_key: str) -> str:
    """Extrae el valor de un campo de Jira manejando diferentes tipos"""
    
    field_value = issue['fields'].get(field_key, '')
    
    # Manejar diferentes tipos de campos
    if field_value is None:
        return ''
    elif isinstance(field_value, dict):
        # Campos tipo objeto (status, issuetype, etc)
        return field_value.get('name', str(field_value))
    elif isinstance(field_value, list):
        # Campos tipo array (labels, components, etc)
        return ', '.join([str(item.get('name', item)) for item in field_value])
    else:
        # Campos simples (string, number, etc)
        return str(field_value)</code></pre>
        </div>

        <div class="bg-green-50 rounded p-4">
          <p class="text-sm font-semibold text-green-700 mb-2">✨ Características Avanzadas:</p>
          <ul class="text-sm space-y-1 list-disc list-inside">
            <li><strong>Paginación automática:</strong> Maneja grandes volúmenes de issues</li>
            <li><strong>Manejo de errores robusto:</strong> Reintentos y mensajes claros</li>
            <li><strong>Progreso en tiempo real:</strong> Actualización continua del estado</li>
            <li><strong>Extracción inteligente:</strong> Maneja diferentes tipos de campos</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Operaciones MySQL -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🗄️ Operaciones MySQL Avanzadas</h3>
      
      <div class="border rounded-lg p-6">
        <h4 class="font-semibold text-gray-900 mb-3">Creación Dinámica de Tablas y Sincronización</h4>
        
        <div class="bg-gray-50 rounded p-4 mb-3">
          <p class="text-sm font-semibold mb-2">Crear Tabla Dinámicamente:</p>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>import mysql.connector
from mysql.connector import Error

def create_mysql_table(conn, config: dict, task_id: str):
    """Crea o actualiza la tabla MySQL con las columnas necesarias"""
    
    cursor = conn.cursor()
    table_name = config['mysql_table']
    
    try:
        # Crear tabla si no existe
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            jira_key VARCHAR(50) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        
        # Obtener columnas existentes
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
        existing_columns = {row[0] for row in cursor.fetchall()}
        
        # Agregar columnas dinámicamente según el mapeo
        for jira_field, mysql_column in config['fields'].items():
            if mysql_column not in existing_columns:
                # Determinar tipo de columna (por defecto TEXT)
                column_type = 'TEXT'
                if mysql_column in ['id', 'key']:
                    column_type = 'VARCHAR(50)'
                elif mysql_column in ['created', 'updated']:
                    column_type = 'DATETIME'
                
                alter_query = f"ALTER TABLE `{table_name}` ADD COLUMN `{mysql_column}` {column_type}"
                cursor.execute(alter_query)
                
                update_task_status(
                    task_id, 
                    'preparando_tabla',
                    message=f"Agregada columna: {mysql_column}"
                )
        
        conn.commit()
        
    except Error as e:
        conn.rollback()
        raise Exception(f"Error al crear tabla: {str(e)}")
    finally:
        cursor.close()

def sync_to_mysql(conn, issues: list, config: dict, task_id: str):
    """Sincroniza los issues en MySQL usando UPSERT"""
    
    cursor = conn.cursor()
    table_name = config['mysql_table']
    field_mapping = config['fields']
    
    try:
        # Preparar columnas para el INSERT
        mysql_columns = ['jira_key'] + list(field_mapping.values())
        columns_str = ', '.join([f'`{col}`' for col in mysql_columns])
        placeholders = ', '.join(['%s'] * len(mysql_columns))
        
        # Preparar UPDATE clause para UPSERT
        update_clause = ', '.join([
            f'`{col}` = VALUES(`{col}`)' 
            for col in mysql_columns if col != 'jira_key'
        ])
        
        # Query UPSERT
        upsert_query = f"""
        INSERT INTO `{table_name}` ({columns_str})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE {update_clause}
        """
        
        # Procesar issues en lotes
        batch_size = 100
        total_issues = len(issues)
        
        for i in range(0, total_issues, batch_size):
            batch = issues[i:i + batch_size]
            values_list = []
            
            for issue in batch:
                # Extraer valores según el mapeo
                values = [issue['key']]  # jira_key
                
                for jira_field, mysql_column in field_mapping.items():
                    value = extract_field_value(issue, jira_field)
                    values.append(value)
                
                values_list.append(values)
            
            # Ejecutar batch insert
            cursor.executemany(upsert_query, values_list)
            
            # Actualizar progreso
            processed = min(i + batch_size, total_issues)
            progress = 50 + int((processed / total_issues) * 40)  # 50-90%
            
            update_task_status(
                task_id,
                'sincronizando',
                progress_percentage=progress,
                processed_issues=processed,
                message=f'Sincronizando en MySQL: {processed}/{total_issues}'
            )
        
        conn.commit()
        
        # Obtener estadísticas
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        total_records = cursor.fetchone()[0]
        
        return {
            'total_synced': total_issues,
            'total_records_in_table': total_records,
            'table_name': table_name
        }
        
    except Error as e:
        conn.rollback()
        raise Exception(f"Error al sincronizar: {str(e)}")
    finally:
        cursor.close()</code></pre>
        </div>

        <div class="bg-indigo-50 rounded p-4">
          <p class="text-sm font-semibold text-indigo-700 mb-2">🚀 Optimizaciones Implementadas:</p>
          <ul class="text-sm space-y-1 list-disc list-inside">
            <li><strong>UPSERT pattern:</strong> INSERT ON DUPLICATE KEY UPDATE</li>
            <li><strong>Batch processing:</strong> Inserciones en lotes de 100</li>
            <li><strong>Columnas dinámicas:</strong> Se crean según necesidad</li>
            <li><strong>Transacciones:</strong> Rollback en caso de error</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Sistema de Backups -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">💾 Sistema de Backups SQL</h3>
      
      <div class="border rounded-lg p-6">
        <h4 class="font-semibold text-gray-900 mb-3">Generación de Respaldos SQL</h4>
        
        <div class="bg-gray-50 rounded p-4 mb-3">
          <p class="text-sm font-semibold mb-2">Implementación del Sistema de Backups:</p>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>import os
from datetime import datetime

def generate_backup(conn, config: dict, task_id: str) -> str:
    """Genera un archivo SQL de respaldo de la tabla"""
    
    cursor = conn.cursor()
    table_name = config['mysql_table']
    
    try:
        # Crear directorio de backups si no existe
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generar nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{table_name}_backup_{timestamp}.sql"
        filepath = os.path.join(backup_dir, filename)
        
        update_task_status(
            task_id,
            'generando_respaldo',
            progress_percentage=95,
            message='Generando archivo de respaldo SQL...'
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Escribir header
            f.write(f"-- Backup de {table_name}\n")
            f.write(f"-- Fecha: {datetime.now().isoformat()}\n")
            f.write(f"-- Total de registros: {get_table_count(cursor, table_name)}\n\n")
            
            # Escribir DROP TABLE IF EXISTS
            f.write(f"DROP TABLE IF EXISTS `{table_name}_backup`;\n\n")
            
            # Obtener y escribir CREATE TABLE
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
            create_statement = cursor.fetchone()[1]
            create_statement = create_statement.replace(
                f"CREATE TABLE `{table_name}`",
                f"CREATE TABLE `{table_name}_backup`"
            )
            f.write(f"{create_statement};\n\n")
            
            # Escribir datos con paginación
            batch_size = 1000
            offset = 0
            
            while True:
                cursor.execute(
                    f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s",
                    (batch_size, offset)
                )
                rows = cursor.fetchall()
                
                if not rows:
                    break
                
                # Obtener nombres de columnas
                column_names = [desc[0] for desc in cursor.description]
                columns_str = ', '.join([f'`{col}`' for col in column_names])
                
                # Escribir INSERT statements
                f.write(f"INSERT INTO `{table_name}_backup` ({columns_str}) VALUES\n")
                
                for i, row in enumerate(rows):
                    values = []
                    for value in row:
                        if value is None:
                            values.append('NULL')
                        elif isinstance(value, (int, float)):
                            values.append(str(value))
                        else:
                            # Escapar strings
                            escaped = str(value).replace("'", "''")
                            values.append(f"'{escaped}'")
                    
                    values_str = ', '.join(values)
                    separator = ';' if i == len(rows) - 1 else ','
                    f.write(f"({values_str}){separator}\n")
                
                f.write("\n")
                offset += batch_size
        
        # Obtener tamaño del archivo
        file_size = os.path.getsize(filepath)
        
        update_task_status(
            task_id,
            'generando_respaldo',
            progress_percentage=98,
            message=f'Respaldo generado: {filename} ({format_file_size(file_size)})'
        )
        
        return filename
        
    except Exception as e:
        raise Exception(f"Error al generar backup: {str(e)}")
    finally:
        cursor.close()

# Endpoints para gestión de backups
@app.get("/backups")
async def list_backups():
    """Lista todos los archivos de backup disponibles"""
    backup_dir = "backups"
    
    if not os.path.exists(backup_dir):
        return {"backups": []}
    
    backups = []
    for filename in os.listdir(backup_dir):
        if filename.endswith('.sql'):
            filepath = os.path.join(backup_dir, filename)
            stat = os.stat(filepath)
            
            backups.append({
                "filename": filename,
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat()
            })
    
    # Ordenar por fecha de creación (más reciente primero)
    backups.sort(key=lambda x: x['created_at'], reverse=True)
    
    return {"backups": backups}

@app.get("/backups/{filename}")
async def download_backup(filename: str):
    """Descarga un archivo de backup específico"""
    filepath = os.path.join("backups", filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Backup not found")
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type='application/sql'
    )</code></pre>
        </div>
      </div>
    </div>

    <!-- Logging y Persistencia -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">📊 Sistema de Logs y Persistencia</h3>
      
      <div class="border rounded-lg p-6">
        <h4 class="font-semibold text-gray-900 mb-3">Tabla de Logs de Sincronización</h4>
        
        <div class="bg-gray-50 rounded p-4 mb-3">
          <p class="text-sm font-semibold mb-2">Implementación del Sistema de Logs:</p>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code># Crear tabla de logs si no existe
def create_sync_logs_table(conn):
    """Crea la tabla de logs de sincronización"""
    cursor = conn.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sync_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_id VARCHAR(36) UNIQUE NOT NULL,
        started_at DATETIME NOT NULL,
        completed_at DATETIME,
        status VARCHAR(50),
        jql_query TEXT,
        total_issues INT DEFAULT 0,
        processed_issues INT DEFAULT 0,
        error_message TEXT,
        result JSON,
        backup_file VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()

def save_sync_log(conn, task_data: dict):
    """Guarda el log de sincronización en la base de datos"""
    cursor = conn.cursor()
    
    try:
        insert_query = """
        INSERT INTO sync_logs (
            task_id, started_at, completed_at, status,
            jql_query, total_issues, processed_issues,
            error_message, result, backup_file
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            task_data['task_id'],
            task_data['started_at'],
            task_data.get('completed_at'),
            task_data['status'],
            task_data.get('jql_query', ''),
            task_data.get('total_issues', 0),
            task_data.get('processed_issues', 0),
            task_data.get('error'),
            json.dumps(task_data.get('result')) if task_data.get('result') else None,
            task_data.get('backup_file')
        )
        
        cursor.execute(insert_query, values)
        conn.commit()
        
    except Error as e:
        print(f"Error al guardar log: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()

# Endpoints para consultar logs
@app.get("/sync-logs")
async def get_sync_logs(
    limit: int = 10,
    offset: int = 0
):
    """Obtiene los logs de sincronización con paginación"""
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Obtener total de registros
        cursor.execute("SELECT COUNT(*) as total FROM sync_logs")
        total = cursor.fetchone()['total']
        
        # Obtener logs paginados
        query = """
        SELECT * FROM sync_logs 
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, offset))
        logs = cursor.fetchall()
        
        # Convertir datetime a string
        for log in logs:
            for key in ['started_at', 'completed_at', 'created_at']:
                if log.get(key):
                    log[key] = log[key].isoformat()
            
            # Parsear JSON result si existe
            if log.get('result') and isinstance(log['result'], str):
                try:
                    log['result'] = json.loads(log['result'])
                except:
                    pass
        
        return {
            "total": total,
            "logs": logs,
            "limit": limit,
            "offset": offset
        }
        
    finally:
        cursor.close()
        conn.close()</code></pre>
        </div>
      </div>
    </div>

    <!-- Manejo de Errores y Mejores Prácticas -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🛡️ Manejo de Errores y Mejores Prácticas</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">Exception Handlers Globales</h4>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request, 
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request, 
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )</code></pre>
        </div>

        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">Connection Pool para MySQL</h4>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>from mysql.connector import pooling

# Configurar pool de conexiones
dbconfig = {
    "pool_name": "mypool",
    "pool_size": 5,
    "pool_reset_session": True,
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "jiradb")
}

# Crear pool global
connection_pool = pooling.MySQLConnectionPool(**dbconfig)

def get_connection_from_pool():
    """Obtiene una conexión del pool"""
    try:
        return connection_pool.get_connection()
    except Error as e:
        print(f"Error getting connection: {e}")
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )</code></pre>
        </div>
      </div>
    </div>

    <!-- Cómo Añadir Nueva Funcionalidad -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🚀 Añadir Nueva Funcionalidad - Ejemplo Práctico</h3>
      
      <div class="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg p-6">
        <h4 class="font-semibold text-gray-900 mb-4">Ejemplo: Añadir Sistema de Webhooks</h4>
        
        <div class="space-y-4">
          <div class="bg-white rounded p-4 border border-orange-200">
            <p class="font-semibold text-orange-700 mb-2">Paso 1: Crear Modelo de Webhook</p>
            <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code># Modelo para registro de webhook
class WebhookConfig(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    url: str = Field(..., regex="^https?://")
    events: List[str] = Field(..., min_items=1)
    active: bool = True
    secret: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com/webhook",
                "events": ["sync.started", "sync.completed", "sync.failed"],
                "secret": "webhook-secret-key"
            }
        }

# Almacenar webhooks en memoria (o base de datos)
webhooks_store: Dict[str, WebhookConfig] = {}</code></pre>
          </div>

          <div class="bg-white rounded p-4 border border-orange-200">
            <p class="font-semibold text-orange-700 mb-2">Paso 2: Endpoints para Gestión de Webhooks</p>
            <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>@app.post("/webhooks", response_model=WebhookConfig)
async def create_webhook(webhook: WebhookConfig):
    """Registra un nuevo webhook"""
    webhooks_store[webhook.id] = webhook
    return webhook

@app.get("/webhooks", response_model=List[WebhookConfig])
async def list_webhooks():
    """Lista todos los webhooks registrados"""
    return list(webhooks_store.values())

@app.delete("/webhooks/{webhook_id}")
async def delete_webhook(webhook_id: str):
    """Elimina un webhook"""
    if webhook_id not in webhooks_store:
        raise HTTPException(404, "Webhook not found")
    
    del webhooks_store[webhook_id]
    return {"message": "Webhook deleted"}</code></pre>
          </div>

          <div class="bg-white rounded p-4 border border-orange-200">
            <p class="font-semibold text-orange-700 mb-2">Paso 3: Integrar con el Sistema Existente</p>
            <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>import httpx
import hmac
import hashlib

async def trigger_webhooks(event: str, data: dict):
    """Dispara webhooks para un evento específico"""
    
    for webhook in webhooks_store.values():
        if not webhook.active or event not in webhook.events:
            continue
        
        payload = {
            "event": event,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        headers = {"Content-Type": "application/json"}
        
        # Agregar firma si hay secret
        if webhook.secret:
            signature = hmac.new(
                webhook.secret.encode(),
                json.dumps(payload).encode(),
                hashlib.sha256
            ).hexdigest()
            headers["X-Webhook-Signature"] = signature
        
        # Enviar webhook de forma asíncrona
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    webhook.url,
                    json=payload,
                    headers=headers,
                    timeout=10.0
                )
            except Exception as e:
                print(f"Error enviando webhook: {e}")

# Modificar la función de sincronización
def sync_jira_to_mysql_background(task_id: str, config: dict):
    try:
        # Trigger webhook de inicio
        asyncio.run(trigger_webhooks("sync.started", {
            "task_id": task_id,
            "config": {k: v for k, v in config.items() 
                      if k not in ['jira_api_token', 'mysql_password']}
        }))
        
        # ... proceso de sincronización ...
        
        # Trigger webhook de completado
        asyncio.run(trigger_webhooks("sync.completed", {
            "task_id": task_id,
            "total_issues": total_issues,
            "duration": duration
        }))
        
    except Exception as e:
        # Trigger webhook de error
        asyncio.run(trigger_webhooks("sync.failed", {
            "task_id": task_id,
            "error": str(e)
        }))</code></pre>
          </div>
        </div>
      </div>
    </div>

    <!-- Testing y Deployment -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🧪 Testing y Deployment</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">Testing con pytest</h4>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code># test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_sync_validation():
    # Test con datos inválidos
    response = client.post("/sync-jira-issues", json={
        "jira_email": "invalid-email"
    })
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_webhook_creation():
    webhook_data = {
        "url": "https://example.com/hook",
        "events": ["sync.completed"]
    }
    response = client.post("/webhooks", json=webhook_data)
    assert response.status_code == 200
    assert response.json()["url"] == webhook_data["url"]</code></pre>
        </div>
        
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">Docker Deployment</h4>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code># Dockerfile optimizado
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear directorio de backups
RUN mkdir -p backups

# Usuario no-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]</code></pre>
        </div>
      </div>
    </div>

    <!-- Recursos y Próximos Pasos -->
    <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-6">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">📚 Recursos y Próximos Pasos</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h4 class="font-semibold text-gray-900 mb-2">Documentación Esencial</h4>
          <ul class="text-sm space-y-1">
            <li>📖 <a href="https://fastapi.tiangolo.com/" class="text-indigo-600 hover:underline" target="_blank">FastAPI Documentation</a></li>
            <li>📖 <a href="https://docs.python.org/3/library/asyncio.html" class="text-indigo-600 hover:underline" target="_blank">Python Asyncio</a></li>
            <li>📖 <a href="https://developer.atlassian.com/cloud/jira/platform/rest/v3/" class="text-indigo-600 hover:underline" target="_blank">Jira REST API v3</a></li>
            <li>📖 <a href="https://dev.mysql.com/doc/" class="text-indigo-600 hover:underline" target="_blank">MySQL Documentation</a></li>
          </ul>
        </div>
        
        <div>
          <h4 class="font-semibold text-gray-900 mb-2">Ideas para Extender el Backend</h4>
          <ul class="text-sm space-y-1">
            <li>🚀 Implementar GraphQL con Strawberry</li>
            <li>🚀 Añadir Redis para caché y queues</li>
            <li>🚀 WebSockets para actualizaciones real-time</li>
            <li>🚀 Integración con Slack/Teams</li>
            <li>🚀 Sistema de plugins extensible</li>
            <li>🚀 Métricas con Prometheus</li>
          </ul>
        </div>
      </div>

      <div class="mt-6 p-4 bg-white rounded border border-purple-200">
        <p class="text-sm text-gray-700">
          <strong>🎯 Siguiente Paso Recomendado:</strong> 
          Implementa un sistema de autenticación con JWT tokens para proteger los endpoints sensibles. 
          Esto preparará tu API para uso en producción con múltiples usuarios.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Component logic for Backend Masterclass
</script>

<style scoped>
pre code {
  @apply block;
}
</style>
