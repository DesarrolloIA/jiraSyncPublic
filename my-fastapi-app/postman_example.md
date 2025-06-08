# Testing Background Sync with Postman

## 1. Start Background Sync

**Request:**
- Method: `POST`
- URL: `http://localhost:8000/sync-jira-issues`
- Headers: `Content-Type: application/json`
- Body:
```json
{
    "jira_domain": "lla.atlassian.net",
    "jira_email": "josue.gomez@libertypr.com",
    "jira_api_token": "your-token-here",
    "jql": "project = SAC",
    "fields": {
        "summary": "resumen",
        "status": "estado",
        "priority": "prioridad",
        "assignee": "asignado_a",
        "customfield_10860": "tipo_cliente"
    },
    "mysql_host": "localhost",
    "mysql_port": 3306,
    "mysql_user": "root",
    "mysql_password": "",
    "mysql_database": "jiradb",
    "mysql_table": "jira_issues",
    "max_results_per_page": 50
}
```

**Response:**
```json
{
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "Sincronización iniciada en segundo plano",
    "status_url": "/sync-status/123e4567-e89b-12d3-a456-426614174000"
}
```

## 2. Check Progress

**Request:**
- Method: `GET`
- URL: `http://localhost:8000/sync-status/{task_id}`
  (Replace {task_id} with the actual ID from step 1)

**Response Examples:**

### While downloading (0-50%):
```json
{
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "descargando",
    "progress_percentage": 25,
    "total_issues": 200,
    "processed_issues": 0,
    "message": "Descargando issues: 50/200",
    "started_at": "2024-01-15T10:30:00.123456",
    "completed_at": null,
    "error": null,
    "result": null
}
```

### While syncing to DB (50-100%):
```json
{
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "sincronizando",
    "progress_percentage": 75,
    "total_issues": 200,
    "processed_issues": 100,
    "message": "Sincronizando: 100/200 issues",
    "started_at": "2024-01-15T10:30:00.123456",
    "completed_at": null,
    "error": null,
    "result": null
}
```

### When completed:
```json
{
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "completado",
    "progress_percentage": 100,
    "total_issues": 200,
    "processed_issues": 200,
    "message": "Sincronización completada: 200 issues procesados",
    "started_at": "2024-01-15T10:30:00.123456",
    "completed_at": "2024-01-15T10:32:30.456789",
    "error": null,
    "result": {
        "total_issues": 200,
        "synced_issues": 200,
        "approximate_count": 200
    }
}
```

### If error occurs:
```json
{
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "error",
    "progress_percentage": 0,
    "total_issues": 0,
    "processed_issues": 0,
    "message": "Error: Connection refused to MySQL",
    "started_at": "2024-01-15T10:30:00.123456",
    "completed_at": "2024-01-15T10:30:05.789012",
    "error": "Connection refused to MySQL",
    "result": null
}
```

## 3. List All Tasks

**Request:**
- Method: `GET`
- URL: `http://localhost:8000/sync-tasks?limit=5`

**Response:**
```json
{
    "tasks": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "status": "completado",
            "progress": 100,
            "total_issues": 200,
            "processed_issues": 200,
            "message": "Sincronización completada: 200 issues procesados",
            "started_at": "2024-01-15T10:30:00.123456",
            "completed_at": "2024-01-15T10:32:30.456789",
            "error": null,
            "result": {...}
        },
        {
            "id": "456e7890-e89b-12d3-a456-426614174111",
            "status": "sincronizando",
            "progress": 65,
            "total_issues": 150,
            "processed_issues": 98,
            "message": "Sincronizando: 98/150 issues",
            "started_at": "2024-01-15T10:35:00.123456",
            "completed_at": null,
            "error": null,
            "result": null
        }
    ],
    "total": 15
}
```

## Tips for Testing:

1. **Start multiple syncs** to see them running in parallel
2. **Use different JQLs** like:
   - `project = SAC AND created >= -7d` (last 7 days)
   - `project = SAC AND status = "In Progress"`
   - `key in (SAC-123, SAC-124, SAC-125)` (specific issues)
3. **Monitor progress** by calling the status endpoint every 2-3 seconds
4. **Check the MySQL database** to verify data is being inserted/updated correctly 