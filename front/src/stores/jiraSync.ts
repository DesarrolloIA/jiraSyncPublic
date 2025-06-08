import { defineStore } from 'pinia'
import axios from 'axios'
import { ref, computed } from 'vue'

export interface JiraSyncConfig {
  jira_domain: string
  jira_email: string
  jira_api_token: string
  jql: string
  fields: Record<string, string>
  mysql_host: string
  mysql_port: number
  mysql_user: string
  mysql_password: string
  mysql_database: string
  mysql_table: string
  max_results_per_page: number
}

export interface SyncTask {
  task_id: string
  status: 'iniciando' | 'obteniendo_total' | 'conectando_db' | 'descargando' | 'preparando_tabla' | 'sincronizando' | 'generando_respaldo' | 'completado' | 'error'
  progress_percentage: number
  total_issues: number
  processed_issues: number
  message: string
  started_at: string
  completed_at: string | null
  error: string | null
  result: any | null
  backup_file?: string
  backup_path?: string
  backup_absolute_path?: string
  backup_size?: number
  backup_url?: string
}

export interface Backup {
  filename: string
  size: number
  created_at: string
  task_id: string
}

export interface SyncLog {
  id: number
  task_id: string
  started_at: string
  completed_at: string | null
  status: string
  jql_query: string
  total_issues: number
  processed_issues: number
  error_message: string | null
  result: any | null
  backup_file: string | null
  created_at: string
}

export const useJiraSyncStore = defineStore('jiraSync', () => {
  // API base URL - use relative path in production
  const API_BASE_URL = import.meta.env.PROD ? '/api' : 'http://127.0.0.1:8000'
  
  // State
  const currentTask = ref<SyncTask | null>(null)
  const isPolling = ref(false)
  const pollingInterval = ref<number | null>(null)
  const syncHistory = ref<SyncTask[]>([])
  const isStartingSync = ref(false)
  
  // Default configuration
  const defaultConfig = ref<JiraSyncConfig>({
    jira_domain: 'lla.atlassian.net',
    jira_email: '',
    jira_api_token: '',
    jql: 'project = SAC AND updated >= -7d',
    fields: {
      summary: 'resumen',
      status: 'estado',
      description: 'descripcion'
    },
    mysql_host: 'localhost',
    mysql_port: 3306,
    mysql_user: 'root',
    mysql_password: '',
    mysql_database: 'jiradb',
    mysql_table: 'jira_issues',
    max_results_per_page: 50
  })
  
  // Computed
  const isRunning = computed(() => {
    return currentTask.value && 
           !['completado', 'error'].includes(currentTask.value.status)
  })
  
  const statusColor = computed(() => {
    if (!currentTask.value) return 'gray'
    
    const colors: Record<string, string> = {
      iniciando: 'blue',
      obteniendo_total: 'blue',
      conectando_db: 'indigo',
      descargando: 'yellow',
      preparando_tabla: 'purple',
      sincronizando: 'green',
      generando_respaldo: 'cyan',
      completado: 'green',
      error: 'red'
    }
    
    return colors[currentTask.value.status] || 'gray'
  })
  
  // Actions
  async function startSync(config: JiraSyncConfig) {
    try {
      isStartingSync.value = true
      
      const response = await axios.post(`${API_BASE_URL}/sync-jira-issues`, config)
      const { task_id } = response.data
      
      // Start polling for progress
      startPolling(task_id)
      
      return task_id
    } catch (error: any) {
      console.error('Error starting sync:', error)
      throw new Error(error.response?.data?.detail || 'Error al iniciar sincronización')
    } finally {
      isStartingSync.value = false
    }
  }
  
  async function checkStatus(taskId: string) {
    try {
      const response = await axios.get(`${API_BASE_URL}/sync-status/${taskId}`)
      currentTask.value = response.data
      
      // If task is completed or errored, stop polling
      if (currentTask.value && ['completado', 'error'].includes(currentTask.value.status)) {
        stopPolling()
        // Add to history
        syncHistory.value.unshift(currentTask.value)
      }
      
      return currentTask.value
    } catch (error) {
      console.error('Error checking status:', error)
      throw error
    }
  }
  
  function startPolling(taskId: string) {
    if (isPolling.value) return
    
    isPolling.value = true
    
    // Initial check
    checkStatus(taskId)
    
    // Poll every 2 seconds
    pollingInterval.value = window.setInterval(() => {
      checkStatus(taskId)
    }, 2000)
  }
  
  function stopPolling() {
    if (pollingInterval.value) {
      clearInterval(pollingInterval.value)
      pollingInterval.value = null
    }
    isPolling.value = false
  }
  
  async function loadSyncHistory() {
    try {
      const response = await axios.get(`${API_BASE_URL}/sync-tasks`)
      syncHistory.value = response.data.tasks
    } catch (error) {
      console.error('Error loading sync history:', error)
    }
  }
  
  function clearCurrentTask() {
    currentTask.value = null
    stopPolling()
  }
  
  // Field management
  function addField(jiraField: string, dbField: string) {
    defaultConfig.value.fields[jiraField] = dbField
  }
  
  function removeField(jiraField: string) {
    delete defaultConfig.value.fields[jiraField]
  }
  
  async function deleteTask(taskId: string) {
    try {
      await axios.delete(`${API_BASE_URL}/sync-tasks/${taskId}`)
      // Remove from history if exists
      const index = syncHistory.value.findIndex(task => task.task_id === taskId)
      if (index > -1) {
        syncHistory.value.splice(index, 1)
      }
      // Clear current task if it's the one being deleted
      if (currentTask.value?.task_id === taskId) {
        clearCurrentTask()
      }
    } catch (error) {
      console.error('Error deleting task:', error)
      throw error
    }
  }
  
  async function loadBackups() {
    try {
      const response = await axios.get(`${API_BASE_URL}/backups`)
      return response.data
    } catch (error) {
      console.error('Error loading backups:', error)
      throw error
    }
  }
  
  async function deleteBackup(filename: string) {
    try {
      await axios.delete(`${API_BASE_URL}/backups/${filename}`)
    } catch (error) {
      console.error('Error deleting backup:', error)
      throw error
    }
  }
  
  function downloadBackup(filename: string) {
    window.open(`${API_BASE_URL}/backups/${filename}`, '_blank')
  }
  
  async function getAllSyncLogs(limit = 10, offset = 0) {
    try {
      const response = await axios.get(`${API_BASE_URL}/sync-logs?limit=${limit}&offset=${offset}`)
      return response.data
    } catch (error) {
      console.error('Error loading sync logs:', error)
      throw error
    }
  }
  
  async function testMySQLConnection(config: JiraSyncConfig): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/test-mysql-connection`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(config),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Error al probar conexión')
      }

      return true
    } catch (error) {
      console.error('Error testing MySQL connection:', error)
      return false
    }
  }



  async function getSyncLogDetails(taskId: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/sync-logs/${taskId}`)
      
      if (!response.ok) {
        throw new Error('Error al obtener detalles')
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('Error getting sync log details:', error)
      throw error
    }
  }

  function getBackupDownloadUrl(filename: string): string {
    return `${API_BASE_URL}/backups/${filename}`
  }
  
  function getApiUrl(): string {
    return API_BASE_URL
  }
  
  return {
    // State
    currentTask,
    isPolling,
    syncHistory,
    isStartingSync,
    defaultConfig,
    
    // Computed
    isRunning,
    statusColor,
    
    // Actions
    startSync,
    checkStatus,
    startPolling,
    stopPolling,
    loadSyncHistory,
    clearCurrentTask,
    addField,
    removeField,
    deleteTask,
    loadBackups,
    deleteBackup,
    downloadBackup,
    getAllSyncLogs,
    testMySQLConnection,
    getSyncLogDetails,
    getBackupDownloadUrl,
    getApiUrl
  }
}) 