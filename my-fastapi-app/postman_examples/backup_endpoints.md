# Endpoints de Verificación de Backups

## 1. Verificar todos los backups
**GET** `http://localhost:8000/api/backups/verify`

Este endpoint muestra:
- La ruta completa del directorio de backups en el servidor
- Lista de todos los archivos SQL con sus rutas completas
- Información detallada de cada archivo (tamaño, fechas, permisos)

### Respuesta esperada:
```json
{
  "backups_directory": "C:\\Users\\Rentas15308\\Documents\\AWS\\script\\2-jiraSync\\my-fastapi-app\\backups",
  "directory_exists": true,
  "is_directory": true,
  "backups": [
    {
      "filename": "jira_sync_2025-06-08_03-04-23.sql",
      "full_path": "C:\\Users\\Rentas15308\\Documents\\AWS\\script\\2-jiraSync\\my-fastapi-app\\backups\\jira_sync_2025-06-08_03-04-23.sql",
      "relative_path": "backups\\jira_sync_2025-06-08_03-04-23.sql",
      "size_bytes": 1853440,
      "size_mb": 1.77,
      "created_at": "2025-06-08T03:04:23",
      "modified_at": "2025-06-08T03:04:23",
      "is_file": true,
      "exists": true,
      "readable": true,
      "writable": true
    }
  ],
  "summary": {
    "total_backups": 5,
    "total_size_mb": 8.85,
    "working_directory": "C:\\Users\\Rentas15308\\Documents\\AWS\\script\\2-jiraSync\\my-fastapi-app",
    "python_version": "3.9.0",
    "platform": "win32"
  }
}
```

## 2. Verificar un backup específico
**GET** `http://localhost:8000/api/backups/check/jira_sync_2025-06-08_03-04-23.sql`

Verifica si un archivo específico existe y muestra:
- Ruta completa en el servidor
- Preview de las primeras líneas del archivo
- URL de descarga

### Respuesta esperada:
```json
{
  "exists": true,
  "filename": "jira_sync_2025-06-08_03-04-23.sql",
  "full_path": "C:\\Users\\Rentas15308\\Documents\\AWS\\script\\2-jiraSync\\my-fastapi-app\\backups\\jira_sync_2025-06-08_03-04-23.sql",
  "relative_path": "backups\\jira_sync_2025-06-08_03-04-23.sql",
  "size_bytes": 1853440,
  "size_mb": 1.77,
  "created_at": "2025-06-08T03:04:23",
  "modified_at": "2025-06-08T03-04-23",
  "is_file": true,
  "readable": true,
  "writable": true,
  "preview": [
    "-- MySQL Backup",
    "-- Database: jiradb",
    "-- Table: jira_issues",
    "-- Generated: 2025-06-08 03:04:23",
    "..."
  ],
  "download_url": "/backups/jira_sync_2025-06-08_03-04-23.sql"
}
```

## 3. Crear un backup de prueba
**POST** `http://localhost:8000/api/backups/create-test`

**Headers:**
```
Content-Type: application/json
```

**Body:** `{}`

Crea un archivo de prueba para verificar que el sistema de backups funciona correctamente.

### Respuesta esperada:
```json
{
  "success": true,
  "message": "Test backup created successfully",
  "filename": "test_backup_2025-06-08_15-30-45.sql",
  "full_path": "C:\\Users\\Rentas15308\\Documents\\AWS\\script\\2-jiraSync\\my-fastapi-app\\backups\\test_backup_2025-06-08_15-30-45.sql",
  "size_bytes": 298,
  "content_preview": [
    "-- Test Backup File",
    "-- Created: 2025-06-08T15:30:45",
    "-- Purpose: Verify backup system functionality",
    "",
    "CREATE TABLE IF NOT EXISTS test_table ("
  ]
}
```

## Verificación en el servidor/contenedor

Si estás usando Docker, puedes verificar los archivos con estos comandos:

```bash
# Listar contenedores
docker ps

# Acceder al contenedor (reemplaza CONTAINER_ID)
docker exec -it CONTAINER_ID bash

# Navegar al directorio de backups
cd /app/backups

# Listar archivos
ls -la

# Ver el contenido de un archivo
head -n 20 jira_sync_2025-06-08_03-04-23.sql
```

Para Windows (sin Docker):
```powershell
# Navegar al directorio del proyecto
cd C:\Users\Rentas15308\Documents\AWS\script\2-jiraSync\my-fastapi-app

# Listar archivos de backup
dir backups\*.sql

# Ver el tamaño de los archivos
Get-ChildItem -Path backups\*.sql | Select-Object Name, Length, CreationTime
``` 