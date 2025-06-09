<template>
  <div class="min-h-screen bg-gray-50 py-4 sm:py-6 lg:py-8">
    <div class="w-full px-3 sm:px-6 lg:px-8 xl:px-12">
      <!-- Header -->
      <div class="bg-white shadow-sm rounded-lg mb-4 sm:mb-6 lg:mb-8">
        <div class="px-4 sm:px-6 py-3 sm:py-4">
          <div class="flex justify-between items-center mb-8">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">Jira Sync Manager</h1>
              <p class="text-gray-600 mt-1">Sincroniza issues de Jira con tu base de datos MySQL</p>
            </div>
            <div class="flex space-x-3">
              <button
                v-if="hasTableConfigured"
                @click="exportCurrentTable"
                class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
                :disabled="isExporting"
              >
                <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                </svg>
                {{ isExporting ? 'Exportando...' : 'Exportar Tabla' }}
              </button>
              <button
                @click="toggleLogsView"
                class="inline-flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors"
              >
                <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                {{ showLogs ? 'Ver Sincronización' : 'Ver Logs Completos' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Normal sync view -->
      <div v-if="!showLogs" class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
        <!-- Configuration Form -->
        <div class="bg-white shadow rounded-lg p-4 sm:p-6 order-2 lg:order-1">
          <h2 class="text-lg sm:text-xl font-semibold text-gray-900 mb-4 sm:mb-6">Configuración de Sincronización</h2>
          
          <JiraSyncForm 
            :disabled="syncStore.isRunning"
            @submit="handleStartSync"
          />
        </div>

        <!-- Progress Console -->
        <div class="bg-white shadow rounded-lg p-4 sm:p-6 order-1 lg:order-2">
          <h2 class="text-lg sm:text-xl font-semibold text-gray-900 mb-4 sm:mb-6">Consola de Progreso</h2>
          
          <SyncProgressConsole 
            :task="syncStore.currentTask"
            :is-polling="syncStore.isPolling"
            @clear="syncStore.clearCurrentTask"
          />
          
          <!-- Recent Tasks / Sync Logs -->
          <div class="mt-6 sm:mt-8">
            <div class="flex items-center justify-between mb-3 sm:mb-4">
              <h3 class="text-base sm:text-lg font-medium text-gray-900">Historial de Sincronizaciones</h3>
              <button
                @click="loadSyncLogs"
                class="text-sm text-indigo-600 hover:text-indigo-800"
              >
                Recargar
              </button>
            </div>
            
            <div v-if="syncLogs.length > 0" class="space-y-3">
              <div
                v-for="log in syncLogs"
                :key="log.task_id"
                class="bg-gradient-to-r from-gray-50 to-white border border-gray-200 rounded-xl p-4 hover:shadow-md transition-all duration-200 cursor-pointer group"
                @click="showLogDetails(log.task_id)"
              >
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="flex items-center space-x-3">
                      <div class="flex-shrink-0">
                        <div :class="getStatusIconClass(log.status)" class="w-10 h-10 rounded-full flex items-center justify-center">
                          <svg v-if="log.status === 'completado'" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                          </svg>
                          <svg v-else-if="log.status === 'error'" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                          </svg>
                          <svg v-else class="w-5 h-5 text-white animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                          </svg>
                        </div>
                      </div>
                      <div>
                        <div class="flex items-center space-x-2">
                          <p class="text-sm font-semibold text-gray-900">Sincronización #{{ log.task_id.substring(0, 8) }}</p>
                          <span :class="getStatusClass(log.status)" class="text-xs px-2 py-1 rounded-full font-medium">
                            {{ getStatusText(log.status) }}
                          </span>
                        </div>
                        <div class="flex items-center mt-1 space-x-4 text-xs text-gray-500">
                          <span class="flex items-center">
                            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                            </svg>
                            {{ log.processed_issues }}/{{ log.total_issues }} issues
                          </span>
                          <span class="flex items-center">
                            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            {{ formatDate(log.created_at) }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      v-if="log.backup_file"
                      @click.stop="downloadBackup(log.backup_file)"
                      class="p-2 bg-green-100 text-green-600 hover:bg-green-200 rounded-lg transition-colors"
                      title="Descargar respaldo"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                      </svg>
                    </button>
                    <button
                      @click.stop="confirmDeleteLog(log.task_id)"
                      class="p-2 bg-red-100 text-red-600 hover:bg-red-200 rounded-lg transition-colors"
                      title="Eliminar"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else-if="!isLoadingLogs" class="text-center py-4 text-gray-500 text-sm">
              No hay sincronizaciones registradas
            </div>
            
            <div v-if="isLoadingLogs" class="text-center py-4 text-gray-500 text-sm">
              Cargando historial...
            </div>
          </div>
        </div>
      </div>

      <!-- Logs viewer -->
      <div v-else class="bg-white shadow rounded-lg p-4 sm:p-6">
        <SyncLogsViewer />
      </div>
    </div>

    <!-- Detail Modal -->
    <SyncDetailModal
      :is-open="showDetailModal"
      :task-id="selectedTaskId"
      @close="showDetailModal = false"
      @deleted="handleTaskDeleted"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useJiraSyncStore } from '@/stores/jiraSync'
import JiraSyncForm from '@/components/JiraSyncForm.vue'
import SyncProgressConsole from '@/components/SyncProgressConsole.vue'
import SyncDetailModal from '@/components/SyncDetailModal.vue'
import SyncHistoryList from '@/components/SyncHistoryList.vue'
import SyncLogsViewer from '@/components/SyncLogsViewer.vue'

const syncStore = useJiraSyncStore()
const showDetailModal = ref<boolean>(false)
const selectedTaskId = ref<string | null>(null)
const syncLogs = ref<any[]>([])
const isLoadingLogs = ref(false)
const mysqlConnectionTested = ref(false)
const isLoading = ref(false)
const isFormValid = ref(false)
const showJsonInput = ref(false)
const jsonConfig = ref('')
const showImportDialog = ref(false)
const importedFile = ref<File | null>(null)
const autoSaveEnabled = ref(false)
const isExporting = ref(false)
const showLogs = ref(false)

// Check if table is configured
const hasTableConfigured = computed(() => {
  const savedConfig = localStorage.getItem('jiraSyncConfig')
  if (savedConfig) {
    try {
      const config = JSON.parse(savedConfig)
      return !!config.mysql_table
    } catch {
      return false
    }
  }
  return false
})

async function handleStartSync(config: any) {
  try {
    await syncStore.startSync(config)
  } catch (error: any) {
    alert(error.message)
  }
}

async function loadSyncLogs() {
  isLoadingLogs.value = true
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/logs/all`)
    const data = await response.json()
    
    if (data.success && data.logs) {
      // Ordenar por fecha más reciente primero y tomar solo los primeros 5
      syncLogs.value = data.logs
        .sort((a: any, b: any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        .slice(0, 5)
    } else {
      syncLogs.value = []
    }
  } catch (error) {
    console.error('Error loading sync logs:', error)
    syncLogs.value = []
  } finally {
    isLoadingLogs.value = false
  }
}

async function testConnectionAndLoadLogs() {
  const savedConfig = localStorage.getItem('jiraSyncConfig')
  if (savedConfig) {
    try {
      const config = JSON.parse(savedConfig)
      if (config.mysql_host && config.mysql_user && config.mysql_database) {
        const isConnected = await syncStore.testMySQLConnection(config)
        if (isConnected) {
          mysqlConnectionTested.value = true
          await loadSyncLogs()
        }
      }
    } catch (error) {
      console.error('Error testing connection:', error)
    }
  }
}

function showLogDetails(taskId: string) {
  selectedTaskId.value = taskId
  showDetailModal.value = true
}

function downloadBackup(filename: string) {
  window.open(syncStore.getBackupDownloadUrl(filename), '_blank')
}

async function confirmDeleteLog(taskId: string) {
  if (confirm('¿Estás seguro de que deseas eliminar esta sincronización y su respaldo?')) {
    try {
      await syncStore.deleteTask(taskId)
      await loadSyncLogs()
    } catch (error) {
      console.error('Error deleting task:', error)
      alert('Error al eliminar la tarea')
    }
  }
}

function handleTaskDeleted(taskId: string) {
  loadSyncLogs()
}

function getStatusClass(status: string) {
  const statusClasses: Record<string, string> = {
    completado: 'bg-green-100 text-green-800',
    error: 'bg-red-100 text-red-800',
    iniciando: 'bg-blue-100 text-blue-800',
    obteniendo_total: 'bg-blue-100 text-blue-800',
    conectando_db: 'bg-indigo-100 text-indigo-800',
    descargando: 'bg-yellow-100 text-yellow-800',
    preparando_tabla: 'bg-purple-100 text-purple-800',
    sincronizando: 'bg-green-100 text-green-800',
    generando_respaldo: 'bg-cyan-100 text-cyan-800'
  }
  return statusClasses[status] || 'bg-gray-100 text-gray-800'
}

function getStatusIconClass(status: string) {
  const iconClasses: Record<string, string> = {
    completado: 'bg-green-500',
    error: 'bg-red-500',
    iniciando: 'bg-blue-500',
    obteniendo_total: 'bg-blue-500',
    conectando_db: 'bg-indigo-500',
    descargando: 'bg-yellow-500',
    preparando_tabla: 'bg-purple-500',
    sincronizando: 'bg-green-500',
    generando_respaldo: 'bg-cyan-500'
  }
  return iconClasses[status] || 'bg-gray-500'
}

function getStatusText(status: string) {
  const statusTexts: Record<string, string> = {
    completado: 'Completado',
    error: 'Error',
    iniciando: 'Iniciando',
    obteniendo_total: 'Obteniendo total',
    conectando_db: 'Conectando DB',
    descargando: 'Descargando',
    preparando_tabla: 'Preparando',
    sincronizando: 'Sincronizando',
    generando_respaldo: 'Respaldando'
  }
  return statusTexts[status] || status
}

function formatDate(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleString('es-MX', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Export current table
const exportCurrentTable = async () => {
  // Get saved configuration from localStorage
  const savedConfig = localStorage.getItem('jiraSyncConfig')
  if (!savedConfig) {
    alert('No hay configuración guardada para exportar')
    return
  }
  
  const config = JSON.parse(savedConfig)
  if (!config.mysql_table) {
    alert('No hay tabla configurada para exportar')
    return
  }

  isExporting.value = true
  
  try {
    const exportData = {
      mysql_host: config.mysql_host,
      mysql_port: config.mysql_port,
      mysql_user: config.mysql_user,
      mysql_password: config.mysql_password,
      mysql_database: config.mysql_database,
      table_name: config.mysql_table
    }
    
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/export-table`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(exportData)
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Error al exportar tabla')
    }
    
    const result = await response.json()
    
    // Download the file
    if (result.download_url) {
      const downloadUrl = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${result.download_url}`
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = result.filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      // Show success message
      alert(`Tabla ${result.table_name} exportada exitosamente (${result.row_count} filas, ${result.file_size_mb} MB)`)
    }
  } catch (error) {
    console.error('Error exporting table:', error)
    alert(error instanceof Error ? error.message : 'Error al exportar tabla')
  } finally {
    isExporting.value = false
  }
}

const toggleLogsView = () => {
  showLogs.value = !showLogs.value
}

onMounted(() => {
  syncStore.loadSyncHistory()
  testConnectionAndLoadLogs()
})
</script> 