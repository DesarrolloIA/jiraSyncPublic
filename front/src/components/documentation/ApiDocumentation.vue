<template>
  <div class="space-y-8">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Documentación de API</h2>
    
    <!-- Sync Endpoints -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Endpoints de Sincronización</h3>
      
      <div class="space-y-6">
        <!-- POST /sync-jira-issues -->
        <div class="border rounded-lg p-4">
          <div class="flex items-center mb-2">
            <span class="px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded">POST</span>
            <code class="ml-3 font-mono text-sm">/sync-jira-issues</code>
          </div>
          <p class="text-gray-600 mb-3">Inicia una sincronización asíncrona de issues de Jira</p>
          
          <div class="bg-gray-50 rounded p-3 mb-3">
            <p class="text-sm font-semibold mb-2">Request Body:</p>
            <pre class="text-xs overflow-x-auto"><code>{
  "jira_domain": "your-domain.atlassian.net",
  "jira_email": "your-email@example.com",
  "jira_api_token": "your-api-token",
  "jql": "project = TEST",
  "fields": {
    "summary": "resumen",
    "status": "estado"
  },
  "mysql_host": "localhost",
  "mysql_port": 3306,
  "mysql_user": "root",
  "mysql_password": "password",
  "mysql_database": "jiradb",
  "mysql_table": "jira_issues"
}</code></pre>
          </div>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Response:</p>
            <pre class="text-xs overflow-x-auto"><code>{
  "task_id": "uuid-string",
  "message": "Sincronización iniciada en segundo plano",
  "status_url": "/sync-status/uuid-string"
}</code></pre>
          </div>
        </div>

        <!-- GET /sync-status/{task_id} -->
        <div class="border rounded-lg p-4">
          <div class="flex items-center mb-2">
            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded">GET</span>
            <code class="ml-3 font-mono text-sm">/sync-status/{task_id}</code>
          </div>
          <p class="text-gray-600 mb-3">Obtiene el estado actual de una tarea de sincronización</p>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Response:</p>
            <pre class="text-xs overflow-x-auto"><code>{
  "task_id": "uuid-string",
  "status": "completado",
  "progress_percentage": 100,
  "total_issues": 860,
  "processed_issues": 860,
  "message": "Sincronización completada",
  "started_at": "2025-06-08T03:00:00",
  "completed_at": "2025-06-08T03:05:00",
  "error": null,
  "result": {
    "backup_file": "jira_sync_2025-06-08.sql"
  }
}</code></pre>
          </div>
        </div>
      </div>
    </div>

    <!-- Logs Endpoints -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Endpoints de Logs</h3>
      
      <div class="space-y-6">
        <!-- GET /api/logs/all -->
        <div class="border rounded-lg p-4">
          <div class="flex items-center mb-2">
            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded">GET</span>
            <code class="ml-3 font-mono text-sm">/api/logs/all</code>
          </div>
          <p class="text-gray-600 mb-3">Obtiene todos los logs de sincronización</p>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Response:</p>
            <pre class="text-xs overflow-x-auto"><code>{
  "logs": [
    {
      "task_id": "uuid-string",
      "started_at": "2025-06-08T03:00:00",
      "completed_at": "2025-06-08T03:05:00",
      "status": "completado",
      "jql_query": "project = TEST",
      "total_issues": 860,
      "processed_issues": 860,
      "backup_file": "jira_sync_2025-06-08.sql"
    }
  ]
}</code></pre>
          </div>
        </div>

        <!-- DELETE /api/logs/{task_id} -->
        <div class="border rounded-lg p-4">
          <div class="flex items-center mb-2">
            <span class="px-2 py-1 bg-red-100 text-red-800 text-xs font-semibold rounded">DELETE</span>
            <code class="ml-3 font-mono text-sm">/api/logs/{task_id}</code>
          </div>
          <p class="text-gray-600 mb-3">Elimina un log específico y su archivo de backup</p>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Response:</p>
            <pre class="text-xs overflow-x-auto"><code>{
  "message": "Log y archivo de backup eliminados exitosamente"
}</code></pre>
          </div>
        </div>

        <!-- POST /api/logs/reset-table -->
        <div class="border rounded-lg p-4">
          <div class="flex items-center mb-2">
            <span class="px-2 py-1 bg-orange-100 text-orange-800 text-xs font-semibold rounded">POST</span>
            <code class="ml-3 font-mono text-sm">/api/logs/reset-table</code>
          </div>
          <p class="text-gray-600 mb-3">Resetea la tabla de logs (elimina todos los registros)</p>
          
          <div class="bg-orange-50 rounded p-3 mb-3">
            <p class="text-sm font-semibold text-orange-800 mb-2">⚠️ Advertencia:</p>
            <p class="text-sm text-orange-700">Esta acción eliminará permanentemente todos los logs y archivos de backup.</p>
          </div>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Response:</p>
            <pre class="text-xs overflow-x-auto"><code>{
  "message": "Tabla de logs reseteada exitosamente",
  "deleted_count": 42
}</code></pre>
          </div>
        </div>
      </div>
    </div>

    <!-- Backup Endpoints -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Endpoints de Backups</h3>
      
      <div class="space-y-6">
        <!-- GET /api/backups/verify -->
        <div class="border rounded-lg p-4">
          <div class="flex items-center mb-2">
            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded">GET</span>
            <code class="ml-3 font-mono text-sm">/api/backups/verify</code>
          </div>
          <p class="text-gray-600 mb-3">Verifica y lista todos los archivos de backup con información detallada</p>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Response:</p>
            <pre class="text-xs overflow-x-auto"><code>{
  "backup_folder": "./backups",
  "files": [
    {
      "filename": "jira_sync_2025-06-08_03-05-00.sql",
      "size_mb": 2.45,
      "created_date": "2025-06-08T03:05:00",
      "is_valid": true
    }
  ],
  "total_files": 1,
  "total_size_mb": 2.45
}</code></pre>
          </div>
        </div>

        <!-- GET /backups/{filename} -->
        <div class="border rounded-lg p-4">
          <div class="flex items-center mb-2">
            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded">GET</span>
            <code class="ml-3 font-mono text-sm">/backups/{filename}</code>
          </div>
          <p class="text-gray-600 mb-3">Descarga un archivo de backup específico</p>
          
          <div class="bg-gray-50 rounded p-3 mb-3">
            <p class="text-sm font-semibold mb-2">Parámetros:</p>
            <ul class="text-sm space-y-1">
              <li><code class="bg-white px-1 rounded">filename</code> - Nombre del archivo SQL a descargar</li>
            </ul>
          </div>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Response:</p>
            <p class="text-sm">Archivo SQL descargable con headers:</p>
            <pre class="text-xs overflow-x-auto"><code>Content-Type: application/sql
Content-Disposition: attachment; filename="jira_sync_2025-06-08.sql"</code></pre>
          </div>
        </div>
      </div>
    </div>

    <!-- Test Endpoints -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Endpoints de Testing</h3>
      
      <div class="space-y-6">
        <!-- POST /test-jira-connection -->
        <div class="border rounded-lg p-4">
          <div class="flex items-center mb-2">
            <span class="px-2 py-1 bg-purple-100 text-purple-800 text-xs font-semibold rounded">POST</span>
            <code class="ml-3 font-mono text-sm">/test-jira-connection</code>
          </div>
          <p class="text-gray-600 mb-3">Verifica la conexión con Jira antes de sincronizar</p>
          
          <div class="bg-gray-50 rounded p-3 mb-3">
            <p class="text-sm font-semibold mb-2">Request Body:</p>
            <pre class="text-xs overflow-x-auto"><code>{
  "jira_domain": "your-domain.atlassian.net",
  "jira_email": "your-email@example.com",
  "jira_api_token": "your-api-token"
}</code></pre>
          </div>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Response:</p>
            <pre class="text-xs overflow-x-auto"><code>{
  "success": true,
  "message": "Conexión exitosa",
  "user_info": {
    "display_name": "John Doe",
    "email": "john.doe@example.com"
  }
}</code></pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Component logic for API Documentation
</script>

<style scoped>
code {
  @apply font-mono text-sm;
}

pre code {
  @apply block;
}
</style> 