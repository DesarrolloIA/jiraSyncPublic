<template>
  <Teleport to="body">
    <div v-if="isOpen" class="fixed inset-0 z-50 overflow-auto bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <!-- Header -->
        <div class="bg-gray-100 px-6 py-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-800">
              Detalles de Sincronización
            </h2>
            <button
              @click="$emit('close')"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- Content -->
        <div class="p-6 overflow-y-auto max-h-[calc(90vh-8rem)]" v-if="syncLog">
          <!-- Basic Info -->
          <div class="mb-6">
            <h3 class="text-md font-semibold mb-3">Información General</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-600">ID de Tarea:</label>
                <p class="text-sm font-mono">{{ syncLog.task_id }}</p>
              </div>
              <div>
                <label class="text-sm text-gray-600">Estado:</label>
                <span :class="getStatusClass(syncLog.status)" class="inline-block px-2 py-1 text-xs rounded-full">
                  {{ syncLog.status }}
                </span>
              </div>
              <div>
                <label class="text-sm text-gray-600">Issues Totales:</label>
                <p class="text-sm font-semibold">{{ syncLog.total_issues }}</p>
              </div>
              <div>
                <label class="text-sm text-gray-600">Issues Procesados:</label>
                <p class="text-sm font-semibold">{{ syncLog.processed_issues }}</p>
              </div>
              <div>
                <label class="text-sm text-gray-600">Iniciado:</label>
                <p class="text-sm">{{ formatDate(syncLog.created_at) }}</p>
              </div>
              <div>
                <label class="text-sm text-gray-600">Finalizado:</label>
                <p class="text-sm">{{ syncLog.updated_at ? formatDate(syncLog.updated_at) : 'En progreso' }}</p>
              </div>
            </div>
          </div>

          <!-- Configuration -->
          <div class="mb-6" v-if="syncLog.config">
            <h3 class="text-md font-semibold mb-3">Configuración</h3>
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="mb-2">
                <label class="text-sm text-gray-600">JQL Query:</label>
                <p class="text-sm font-mono bg-white p-2 rounded border">{{ syncLog.config.jql }}</p>
              </div>
              <div class="grid grid-cols-2 gap-4 mt-4">
                <div>
                  <label class="text-sm text-gray-600">Base de Datos:</label>
                  <p class="text-sm">{{ syncLog.config.mysql_database }}</p>
                </div>
                <div>
                  <label class="text-sm text-gray-600">Tabla:</label>
                  <p class="text-sm">{{ syncLog.config.mysql_table }}</p>
                </div>
              </div>
              <div class="mt-4" v-if="syncLog.config.fields">
                <label class="text-sm text-gray-600">Mapeo de Campos:</label>
                <div class="mt-2 space-y-1">
                  <div v-for="(dbField, jiraField) in syncLog.config.fields" :key="jiraField" class="text-sm">
                    <span class="font-mono">{{ jiraField }}</span> → <span class="font-mono">{{ dbField }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Backup -->
          <div class="mb-6" v-if="syncLog.backup_file">
            <h3 class="text-md font-semibold mb-3">Respaldo</h3>
            <div class="flex items-center justify-between bg-green-50 p-4 rounded-lg">
              <div>
                <p class="text-sm text-green-800">{{ syncLog.backup_file }}</p>
                <p class="text-xs text-green-600 mt-1">Respaldo SQL generado exitosamente</p>
              </div>
              <button
                @click="downloadBackup"
                class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors text-sm"
              >
                Descargar
              </button>
            </div>
          </div>

          <!-- Error -->
          <div v-if="syncLog.error_message" class="mb-6">
            <h3 class="text-md font-semibold mb-3">Error</h3>
            <div class="bg-red-50 p-4 rounded-lg">
              <p class="text-sm text-red-800 whitespace-pre-wrap">{{ syncLog.error_message }}</p>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="bg-gray-100 px-6 py-4 border-t border-gray-200">
          <div class="flex justify-between">
            <button
              v-if="syncLog && syncLog.status === 'completado'"
              @click="confirmDelete"
              class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors text-sm"
            >
              Eliminar
            </button>
            <button
              @click="$emit('close')"
              class="ml-auto px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 transition-colors text-sm"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useJiraSyncStore } from '@/stores/jiraSync'

const props = defineProps<{
  isOpen: boolean
  taskId: string | null
}>()

const emit = defineEmits<{
  close: []
  deleted: [taskId: string]
}>()

const store = useJiraSyncStore()
const syncLog = ref<any>(null)
const isLoading = ref(false)

// Watch for changes in taskId
watch(() => props.taskId, async (newTaskId) => {
  if (newTaskId && props.isOpen) {
    isLoading.value = true
    try {
      syncLog.value = await store.getSyncLogDetails(newTaskId)
    } catch (error) {
      console.error('Error loading sync details:', error)
    } finally {
      isLoading.value = false
    }
  }
})

function getStatusClass(status: string) {
  const statusClasses: Record<string, string> = {
    completado: 'bg-green-100 text-green-800',
    error: 'bg-red-100 text-red-800',
    iniciando: 'bg-blue-100 text-blue-800',
    default: 'bg-gray-100 text-gray-800'
  }
  return statusClasses[status] || statusClasses.default
}

function formatDate(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleString('es-MX', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

function downloadBackup() {
  if (syncLog.value?.backup_file) {
    window.open(store.getBackupDownloadUrl(syncLog.value.backup_file), '_blank')
  }
}

async function confirmDelete() {
  if (confirm('¿Estás seguro de que deseas eliminar esta sincronización y su respaldo?')) {
    try {
      await store.deleteTask(props.taskId!)
      emit('deleted', props.taskId!)
      emit('close')
    } catch (error) {
      console.error('Error deleting task:', error)
      alert('Error al eliminar la tarea')
    }
  }
}
</script> 