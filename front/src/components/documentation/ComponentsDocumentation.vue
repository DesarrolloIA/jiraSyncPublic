<template>
  <div class="space-y-8">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Documentación de Componentes</h2>
    
    <!-- Frontend Components -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Componentes Frontend (Vue 3)</h3>
      
      <div class="space-y-6">
        <!-- JiraSyncForm -->
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">JiraSyncForm.vue</h4>
          <p class="text-gray-600 mb-3">Formulario principal de configuración para la sincronización</p>
          
          <div class="bg-gray-50 rounded p-3 mb-3">
            <p class="text-sm font-semibold mb-2">Props:</p>
            <ul class="text-sm space-y-1">
              <li><code class="bg-white px-1 rounded">disabled: Boolean</code> - Deshabilita el formulario durante la sincronización</li>
            </ul>
          </div>
          
          <div class="bg-gray-50 rounded p-3 mb-3">
            <p class="text-sm font-semibold mb-2">Emits:</p>
            <ul class="text-sm space-y-1">
              <li><code class="bg-white px-1 rounded">@submit</code> - Emitido cuando se envía el formulario con la configuración</li>
            </ul>
          </div>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Características:</p>
            <ul class="text-sm space-y-1 list-disc list-inside">
              <li>Validación de campos en tiempo real</li>
              <li>Guardado automático en localStorage</li>
              <li>Mapeo dinámico de campos Jira → MySQL</li>
              <li>Import/Export de configuración JSON</li>
            </ul>
          </div>
        </div>

        <!-- SyncProgressConsole -->
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">SyncProgressConsole.vue</h4>
          <p class="text-gray-600 mb-3">Consola tipo terminal que muestra el progreso de sincronización en tiempo real</p>
          
          <div class="bg-gray-50 rounded p-3 mb-3">
            <p class="text-sm font-semibold mb-2">Props:</p>
            <ul class="text-sm space-y-1">
              <li><code class="bg-white px-1 rounded">task: Object</code> - Información de la tarea actual</li>
              <li><code class="bg-white px-1 rounded">isPolling: Boolean</code> - Indica si está consultando el estado</li>
            </ul>
          </div>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Características:</p>
            <ul class="text-sm space-y-1 list-disc list-inside">
              <li>Animación de texto tipo máquina de escribir</li>
              <li>Barra de progreso visual</li>
              <li>Colores dinámicos según el estado</li>
              <li>Auto-scroll para mostrar últimas líneas</li>
            </ul>
          </div>
        </div>

        <!-- SyncLogsViewer -->
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">SyncLogsViewer.vue</h4>
          <p class="text-gray-600 mb-3">Vista completa de logs con interfaz de consola interactiva</p>
          
          <div class="bg-gray-50 rounded p-3 mb-3">
            <p class="text-sm font-semibold mb-2">Métodos principales:</p>
            <ul class="text-sm space-y-1">
              <li><code class="bg-white px-1 rounded">fetchLogs()</code> - Obtiene todos los logs del servidor</li>
              <li><code class="bg-white px-1 rounded">deleteLog(taskId)</code> - Elimina un log específico</li>
              <li><code class="bg-white px-1 rounded">resetTable()</code> - Resetea la tabla completa</li>
              <li><code class="bg-white px-1 rounded">downloadBackup(filename)</code> - Descarga archivo SQL</li>
            </ul>
          </div>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Características:</p>
            <ul class="text-sm space-y-1 list-disc list-inside">
              <li>Lista todos los logs de sincronización</li>
              <li>Acciones: descargar backup, ver detalles, eliminar</li>
              <li>Botón de reset completo de tabla</li>
              <li>Modales de confirmación para acciones destructivas</li>
              <li>Actualización automática al realizar cambios</li>
            </ul>
          </div>
        </div>

        <!-- SyncHistoryList -->
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">SyncHistoryList.vue</h4>
          <p class="text-gray-600 mb-3">Lista de tareas de sincronización recientes</p>
          
          <div class="bg-gray-50 rounded p-3 mb-3">
            <p class="text-sm font-semibold mb-2">Props:</p>
            <ul class="text-sm space-y-1">
              <li><code class="bg-white px-1 rounded">tasks: Array</code> - Lista de tareas recientes</li>
            </ul>
          </div>
          
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Estados mostrados:</p>
            <ul class="text-sm space-y-1 list-disc list-inside">
              <li><span class="text-green-600">✓ Completado</span> - Sincronización exitosa</li>
              <li><span class="text-yellow-600">⚡ En progreso</span> - Sincronización activa</li>
              <li><span class="text-red-600">✗ Error</span> - Sincronización fallida</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Backend Structure -->
    <div>
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Estructura Backend (FastAPI)</h3>
      
      <div class="bg-gray-50 rounded p-4 mb-4">
        <pre class="text-sm overflow-x-auto"><code>my-fastapi-app/
├── main.py              # Aplicación principal con todos los endpoints
├── requirements.txt     # Dependencias Python
├── .env                # Variables de entorno (no versionado)
├── backups/            # Directorio de respaldos SQL
└── postman_examples/   # Ejemplos para testing con Postman
    ├── README.md
    ├── test_connection.json
    └── get_logs_by_task.json</code></pre>
      </div>

      <!-- Main.py Structure -->
      <div class="border rounded-lg p-4">
        <h4 class="font-semibold text-gray-900 mb-2">Estructura de main.py</h4>
        
        <div class="space-y-3">
          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Imports y configuración:</p>
            <pre class="text-xs overflow-x-auto"><code>from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
import requests
import threading
import uuid</code></pre>
          </div>

          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Modelos Pydantic:</p>
            <ul class="text-sm space-y-1">
              <li><code class="bg-white px-1 rounded">JiraConfig</code> - Configuración de Jira</li>
              <li><code class="bg-white px-1 rounded">MySQLConfig</code> - Configuración de MySQL</li>
              <li><code class="bg-white px-1 rounded">SyncRequest</code> - Request completo de sincronización</li>
              <li><code class="bg-white px-1 rounded">TaskStatus</code> - Estado de la tarea</li>
            </ul>
          </div>

          <div class="bg-gray-50 rounded p-3">
            <p class="text-sm font-semibold mb-2">Funciones principales:</p>
            <ul class="text-sm space-y-1">
              <li><code class="bg-white px-1 rounded">get_jira_issues()</code> - Obtiene issues de Jira API</li>
              <li><code class="bg-white px-1 rounded">create_mysql_table()</code> - Crea tabla dinámica</li>
              <li><code class="bg-white px-1 rounded">sync_to_mysql()</code> - Sincroniza datos</li>
              <li><code class="bg-white px-1 rounded">generate_backup()</code> - Genera archivo SQL</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Store Structure -->
    <div class="mt-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Pinia Store (jiraSync.ts)</h3>
      
      <div class="border rounded-lg p-4">
        <div class="bg-gray-50 rounded p-3 mb-3">
          <p class="text-sm font-semibold mb-2">Estado (State):</p>
          <pre class="text-xs overflow-x-auto"><code>interface State {
  tasks: TaskStatus[]
  currentTaskId: string | null
  isPolling: boolean
  pollingInterval: number | null
}</code></pre>
        </div>

        <div class="bg-gray-50 rounded p-3 mb-3">
          <p class="text-sm font-semibold mb-2">Acciones principales:</p>
          <ul class="text-sm space-y-1">
            <li><code class="bg-white px-1 rounded">startSync(config)</code> - Inicia sincronización</li>
            <li><code class="bg-white px-1 rounded">pollTaskStatus(taskId)</code> - Consulta estado</li>
            <li><code class="bg-white px-1 rounded">stopPolling()</code> - Detiene polling</li>
            <li><code class="bg-white px-1 rounded">addTask(task)</code> - Agrega tarea al historial</li>
          </ul>
        </div>

        <div class="bg-gray-50 rounded p-3">
          <p class="text-sm font-semibold mb-2">Getters:</p>
          <ul class="text-sm space-y-1">
            <li><code class="bg-white px-1 rounded">currentTask</code> - Tarea actual en progreso</li>
            <li><code class="bg-white px-1 rounded">recentTasks</code> - Últimas 5 tareas</li>
            <li><code class="bg-white px-1 rounded">hasActiveTasks</code> - Verifica tareas activas</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Component logic for Components Documentation
</script>

<style scoped>
code {
  @apply font-mono text-sm;
}

pre code {
  @apply block;
}
</style> 