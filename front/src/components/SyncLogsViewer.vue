<template>
  <div class="sync-logs-viewer">
    <div class="logs-header">
      <h3 class="text-lg font-semibold">Historial de Sincronizaciones</h3>
      <div class="header-actions">
        <button
          @click="refreshLogs"
          class="btn-action refresh"
          :disabled="loading"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Actualizar
        </button>
        <button
          @click="showResetDialog = true"
          class="btn-action reset"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Reset Tabla
        </button>
      </div>
    </div>

    <div class="logs-console" ref="consoleElement">
      <div class="console-header">
        <div class="console-dots">
          <span class="dot red"></span>
          <span class="dot yellow"></span>
          <span class="dot green"></span>
        </div>
        <span class="console-title">Sync Logs Console v1.0</span>
      </div>
      
      <div class="console-body">
        <div v-if="loading" class="console-line">
          <span class="prompt">$</span> Cargando logs...
        </div>
        
        <div v-else-if="error" class="console-line error">
          <span class="prompt">✗</span> Error: {{ error }}
        </div>
        
        <div v-else-if="logs.length === 0" class="console-line">
          <span class="prompt">$</span> No hay sincronizaciones registradas
        </div>
        
        <div v-else>
          <div class="console-line">
            <span class="prompt">$</span> Total de sincronizaciones: {{ logs.length }}
          </div>
          <div class="console-line">
            <span class="prompt">$</span> ================================
          </div>
          
          <div v-for="(log, index) in logs" :key="log.task_id" class="log-entry">
            <div class="console-line">
              <span class="prompt">[{{ index + 1 }}]</span> Task ID: {{ log.task_id }}
            </div>
            <div class="console-line indent">
              <span class="label">Estado:</span> 
              <span :class="getStatusClass(log.status)">{{ log.status }}</span>
            </div>
            <div class="console-line indent">
              <span class="label">Fecha:</span> {{ formatDate(log.created_at) }}
            </div>
            <div class="console-line indent">
              <span class="label">Issues:</span> {{ log.processed_issues }}/{{ log.total_issues }}
            </div>
            <div v-if="log.backup_file" class="console-line indent">
              <span class="label">Backup:</span> {{ log.backup_file }}
            </div>
            
            <div class="log-actions">
              <button
                @click="downloadBackup(log.backup_file)"
                v-if="log.backup_file"
                class="btn-small download"
                title="Descargar backup"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                </svg>
              </button>
              <button
                @click="viewLogDetails(log)"
                class="btn-small view"
                title="Ver detalles"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
              <button
                @click="confirmDelete(log)"
                class="btn-small delete"
                title="Eliminar"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
            
            <div class="console-line separator">
              <span class="prompt">─</span>────────────────────────────────
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación para reset -->
    <div v-if="showResetDialog" class="modal-overlay" @click="showResetDialog = false">
      <div class="modal-content" @click.stop>
        <h3 class="modal-title">¿Resetear tabla de logs?</h3>
        <p class="modal-text">Esta acción eliminará todos los registros de sincronización y sus archivos de backup asociados.</p>
        <div class="modal-actions">
          <button @click="showResetDialog = false" class="btn-cancel">
            Cancelar
          </button>
          <button @click="resetTable" class="btn-confirm">
            Confirmar Reset
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación para eliminar -->
    <div v-if="showDeleteDialog" class="modal-overlay" @click="showDeleteDialog = false">
      <div class="modal-content" @click.stop>
        <h3 class="modal-title">¿Eliminar sincronización?</h3>
        <p class="modal-text">Se eliminará el registro y el archivo de backup asociado.</p>
        <p class="modal-text-small">Task ID: {{ selectedLog?.task_id }}</p>
        <div class="modal-actions">
          <button @click="showDeleteDialog = false" class="btn-cancel">
            Cancelar
          </button>
          <button @click="deleteLog" class="btn-confirm delete">
            Eliminar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface SyncLog {
  task_id: string
  status: string
  total_issues: number
  processed_issues: number
  created_at: string
  backup_file: string | null
  error_message: string | null
}

const logs = ref<SyncLog[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const showResetDialog = ref(false)
const showDeleteDialog = ref(false)
const selectedLog = ref<SyncLog | null>(null)
const consoleElement = ref<HTMLElement>()

const fetchLogs = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get('http://localhost:8000/api/logs/all')
    
    if (response.data.success && response.data.logs) {
      logs.value = response.data.logs
    } else {
      logs.value = []
      if (response.data.error) {
        error.value = response.data.error
      }
    }
  } catch (err: any) {
    console.error('Error fetching logs:', err)
    error.value = err.response?.data?.detail || 'Error al cargar los logs'
  } finally {
    loading.value = false
  }
}

const refreshLogs = () => {
  fetchLogs()
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString('es-MX')
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'completado':
      return 'status-success'
    case 'error':
      return 'status-error'
    case 'iniciando':
    case 'sincronizando':
      return 'status-progress'
    default:
      return 'status-default'
  }
}

const downloadBackup = (filename: string) => {
  if (!filename) return
  
  const url = `http://localhost:8000/backups/${filename}`
  window.open(url, '_blank')
}

const viewLogDetails = (log: SyncLog) => {
  // TODO: Implementar vista de detalles
  console.log('View details for:', log)
}

const confirmDelete = (log: SyncLog) => {
  selectedLog.value = log
  showDeleteDialog.value = true
}

const deleteLog = async () => {
  if (!selectedLog.value) return
  
  try {
    const response = await axios.delete(`http://localhost:8000/api/logs/${selectedLog.value.task_id}`)
    
    if (response.data.success) {
      showDeleteDialog.value = false
      await fetchLogs()
      
      // Scroll to top of console
      if (consoleElement.value) {
        consoleElement.value.scrollTop = 0
      }
    } else {
      alert('Error al eliminar el log: ' + (response.data.message || 'Error desconocido'))
    }
  } catch (err: any) {
    console.error('Error deleting log:', err)
    alert('Error al eliminar el log: ' + (err.response?.data?.detail || err.message))
  }
}

const resetTable = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/logs/reset-table')
    
    if (response.data.success) {
      showResetDialog.value = false
      await fetchLogs()
      
      // Show success message
      const deletedCount = response.data.deleted_files || 0
      const failedCount = response.data.failed_files || 0
      
      let message = `Tabla reseteada exitosamente.\n`
      message += `Archivos eliminados: ${deletedCount}`
      if (failedCount > 0) {
        message += `\nArchivos con error: ${failedCount}`
      }
      
      alert(message)
    } else {
      alert('Error al resetear la tabla: ' + (response.data.error || 'Error desconocido'))
    }
  } catch (err: any) {
    console.error('Error resetting table:', err)
    alert('Error al resetear la tabla: ' + (err.response?.data?.detail || err.message))
  }
}

onMounted(() => {
  fetchLogs()
})
</script>

<style scoped>
.sync-logs-viewer {
  @apply h-full flex flex-col;
}

.logs-header {
  @apply flex justify-between items-center mb-4;
}

.header-actions {
  @apply flex gap-2;
}

.btn-action {
  @apply px-3 py-2 rounded-lg flex items-center gap-2 text-sm font-medium transition-colors;
}

.btn-action.refresh {
  @apply bg-blue-500 text-white hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed;
}

.btn-action.reset {
  @apply bg-orange-500 text-white hover:bg-orange-600;
}

.logs-console {
  @apply bg-gray-900 rounded-lg overflow-hidden flex-1 flex flex-col;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

.console-header {
  @apply bg-gray-800 px-4 py-2 flex items-center justify-between border-b border-gray-700;
}

.console-dots {
  @apply flex gap-2;
}

.dot {
  @apply w-3 h-3 rounded-full;
}

.dot.red {
  @apply bg-red-500;
}

.dot.yellow {
  @apply bg-yellow-500;
}

.dot.green {
  @apply bg-green-500;
}

.console-title {
  @apply text-gray-400 text-xs;
}

.console-body {
  @apply p-4 text-gray-300 text-sm overflow-y-auto flex-1;
}

.console-line {
  @apply mb-1;
}

.console-line.error {
  @apply text-red-400;
}

.console-line.indent {
  @apply ml-6;
}

.prompt {
  @apply text-green-400 mr-2;
}

.label {
  @apply text-gray-500 mr-2;
}

.status-success {
  @apply text-green-400;
}

.status-error {
  @apply text-red-400;
}

.status-progress {
  @apply text-yellow-400;
}

.status-default {
  @apply text-gray-400;
}

.log-entry {
  @apply mb-3;
}

.log-actions {
  @apply flex gap-2 mt-2 ml-6;
}

.btn-small {
  @apply p-1.5 rounded-md transition-colors;
}

.btn-small.download {
  @apply bg-blue-600 text-white hover:bg-blue-700;
}

.btn-small.view {
  @apply bg-gray-600 text-white hover:bg-gray-700;
}

.btn-small.delete {
  @apply bg-red-600 text-white hover:bg-red-700;
}

.separator {
  @apply text-gray-700 text-xs;
}

/* Modal styles */
.modal-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50;
}

.modal-content {
  @apply bg-white rounded-lg p-6 max-w-md w-full mx-4;
}

.modal-title {
  @apply text-lg font-semibold mb-3;
}

.modal-text {
  @apply text-gray-600 mb-2;
}

.modal-text-small {
  @apply text-sm text-gray-500 mb-4;
}

.modal-actions {
  @apply flex justify-end gap-3 mt-6;
}

.btn-cancel {
  @apply px-4 py-2 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 transition-colors;
}

.btn-confirm {
  @apply px-4 py-2 rounded-lg bg-orange-500 text-white hover:bg-orange-600 transition-colors;
}

.btn-confirm.delete {
  @apply bg-red-500 hover:bg-red-600;
}

/* Responsive */
@media (max-width: 640px) {
  .logs-header {
    @apply flex-col gap-3;
  }
  
  .header-actions {
    @apply w-full;
  }
  
  .btn-action {
    @apply flex-1 justify-center;
  }
}
</style> 