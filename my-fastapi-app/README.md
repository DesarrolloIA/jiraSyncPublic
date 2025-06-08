# Jira to MySQL Sync API

This FastAPI application provides an endpoint to synchronize Jira issues to a MySQL database.

## Features

- **Automatic Issue Count**: First gets the approximate count of issues matching your JQL
- **Pagination Support**: Handles large datasets by paginating through all issues
- **Dynamic Table Creation**: Automatically creates the MySQL table if it doesn't exist
- **Dynamic Column Addition**: Adds new columns to the table as new fields appear in Jira
- **Upsert Logic**: Updates existing issues or inserts new ones based on the issue key
- **Field Type Detection**: Automatically determines appropriate MySQL column types
- **Complex Field Handling**: Flattens nested Jira fields for database storage

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### POST /sync-jira-issues

Synchronizes Jira issues to MySQL database.

**Request Body Example (List Format):**
```json
{
    "jira_domain": "your-domain.atlassian.net",
    "jira_email": "your-email@example.com",
    "jira_api_token": "your-api-token",
    "jql": "project = SAC",
    "fields": ["summary", "status", "priority", "assignee", "created", "updated"],
    "mysql_host": "localhost",
    "mysql_port": 3306,
    "mysql_user": "root",
    "mysql_password": "password",
    "mysql_database": "jira_sync",
    "mysql_table": "jira_issues",
    "max_results_per_page": 50
}
```

**Request Body Example (With Field Mapping):**
```json
{
    "jira_domain": "your-domain.atlassian.net",
    "jira_email": "your-email@example.com",
    "jira_api_token": "your-api-token",
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
    "mysql_password": "password",
    "mysql_database": "jira_sync",
    "mysql_table": "jira_issues"
}
```

**Response Example:**
```json
{
    "success": true,
    "message": "Successfully synced 153 issues",
    "total_issues": 153,
    "approximate_count": 153
}
```

### GET /sync-example

Returns an example of the sync request format.

## How It Works

1. **Issue Count**: Uses Jira's `/rest/api/3/search/approximate-count` endpoint to get the total number of issues
2. **Pagination**: Fetches issues in batches using the `nextPageToken` mechanism
3. **Table Management**: 
   - Creates the table if it doesn't exist
   - Adds new columns dynamically as new fields appear in Jira
   - Uses the issue `key` as the primary key
4. **Data Storage**:
   - Flattens nested Jira objects (e.g., `status.name` becomes `status_name`)
   - Stores complex objects and arrays as JSON
   - Uses `INSERT ... ON DUPLICATE KEY UPDATE` for upsert operations

## Jira API Token

To get your Jira API token:
1. Log in to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name and copy the token

## Field Types

The sync automatically detects and uses appropriate MySQL types:
- Boolean fields → `BOOLEAN`
- Integer fields → `BIGINT`
- Float fields → `DOUBLE`
- Objects/Arrays → `JSON`
- Everything else → `TEXT`

## Testing with Postman

1. Create a new POST request to `http://localhost:8000/sync-jira-issues`
2. Set the Content-Type header to `application/json`
3. Use the example JSON above in the request body
4. Replace the values with your actual Jira and MySQL credentials 

## Field Mapping Feature

You can now map Jira field names to custom column names in your MySQL database. This is useful when you want to use more descriptive names in your database.

### How it works:

1. **List Format** (original):
   ```json
   "fields": ["summary", "status", "customfield_10001"]
   ```
   This will create columns with the same names as in Jira.

2. **Dictionary Format** (with mapping):
   ```json
   "fields": {
       "summary": "resumen",
       "status": "estado_ticket",
       "customfield_10001": "tipo_cliente"
   }
   ```
   This will:
   - Fetch `summary` from Jira → save in column `resumen`
   - Fetch `status` from Jira → save in column `estado_ticket`
   - Fetch `customfield_10001` from Jira → save in column `tipo_cliente`

### Complex Field Mapping:

For fields that contain objects (like status, priority, etc.), the system automatically creates additional columns:
- `status` → creates `estado_ticket` (full JSON) and `estado_ticket_name` (just the name)
- `assignee` → creates `asignado_a` (full JSON) and `asignado_a_name` (just the name) 

## Background Sync with Progress Tracking

The API now supports background synchronization with real-time progress tracking, perfect for frontend applications that need to show progress to users.

### How it works:

1. **Start Sync** - POST `/sync-jira-issues`
   - Returns immediately with a `task_id`
   - The sync runs in the background

2. **Check Progress** - GET `/sync-status/{task_id}`
   - Returns current status and progress percentage
   - Updates in real-time as the sync progresses

3. **List Tasks** - GET `/sync-tasks`
   - Shows recent sync tasks and their status

### Workflow Example:

1. **Start the sync:**
```bash
POST /sync-jira-issues
Response:
{
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "Sincronización iniciada en segundo plano",
    "status_url": "/sync-status/123e4567-e89b-12d3-a456-426614174000"
}
```

2. **Check progress periodically:**
```bash
GET /sync-status/123e4567-e89b-12d3-a456-426614174000
Response:
{
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "sincronizando",
    "progress_percentage": 75,
    "total_issues": 200,
    "processed_issues": 150,
    "message": "Sincronizando: 150/200 issues",
    "started_at": "2024-01-15T10:30:00",
    "completed_at": null,
    "error": null
}
```

### Status Values:

- `iniciando` - Starting the sync process
- `obteniendo_total` - Getting total issue count
- `conectando_db` - Connecting to MySQL
- `descargando` - Downloading issues from Jira (0-50% progress)
- `preparando_tabla` - Preparing MySQL table
- `sincronizando` - Syncing to database (50-100% progress)
- `completado` - Sync completed successfully
- `error` - An error occurred

### Frontend Integration Example (JavaScript):

```javascript
// Start sync
const response = await fetch('/sync-jira-issues', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(syncConfig)
});
const { task_id } = await response.json();

// Poll for progress
const checkProgress = async () => {
    const status = await fetch(`/sync-status/${task_id}`);
    const data = await status.json();
    
    console.log(`Progress: ${data.progress_percentage}%`);
    console.log(`Status: ${data.message}`);
    
    if (data.status !== 'completado' && data.status !== 'error') {
        setTimeout(checkProgress, 2000); // Check every 2 seconds
    }
};

checkProgress();
``` 