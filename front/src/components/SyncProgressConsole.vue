<template>
  <div class="bg-gray-900 rounded-lg p-3 sm:p-4 lg:p-6 text-white font-mono text-xs sm:text-sm">
    <!-- Console Header -->
    <div class="flex items-center justify-between mb-3 sm:mb-4">
      <div class="flex items-center space-x-1.5 sm:space-x-2">
        <div class="w-2.5 h-2.5 sm:w-3 sm:h-3 bg-red-500 rounded-full"></div>
        <div class="w-2.5 h-2.5 sm:w-3 sm:h-3 bg-yellow-500 rounded-full"></div>
        <div class="w-2.5 h-2.5 sm:w-3 sm:h-3 bg-green-500 rounded-full"></div>
      </div>
      <div class="text-gray-400 text-[10px] sm:text-xs">
        Jira Sync Console v1.0
      </div>
    </div>

    <!-- Console Content -->
    <div class="space-y-2 sm:space-y-3 min-h-[200px] sm:min-h-[250px] lg:min-h-[300px] max-h-[400px] sm:max-h-[450px] lg:max-h-[500px] overflow-y-auto">
      <!-- No Task -->
      <div v-if="!task" class="text-gray-500">
        <p>$ Esperando nueva tarea de sincronización...</p>
        <p class="mt-2 animate-pulse">$ _</p>
      </div>

      <!-- Task Running -->
      <div v-else class="space-y-2">
        <!-- Task ID -->
        <div class="text-green-400">
          $ Task ID: {{ task.task_id }}
        </div>

        <!-- Status -->
        <div :class="statusColorClass">
          $ Estado: {{ statusLabel }}
        </div>

        <!-- DEBUG: Raw Status -->
        <div class="text-gray-500 text-[10px] bg-gray-800 p-1 rounded">
          DEBUG: status={{ task.status }} | progress={{ task.progress_percentage }}% | message={{ task.message }}
        </div>

        <!-- Progress Bar -->
        <div v-if="task.progress_percentage > 0" class="space-y-1">
          <div class="text-gray-400">
            $ Progreso: {{ task.progress_percentage }}%
          </div>
          <div class="bg-gray-800 rounded-full h-3 sm:h-4 overflow-hidden">
            <div 
              class="h-full transition-all duration-500 ease-out"
              :class="progressBarColor"
              :style="{ width: `${task.progress_percentage}%` }"
            >
              <div class="h-full bg-gradient-to-r from-transparent to-white/20"></div>
            </div>
          </div>
        </div>

        <!-- Issues Count -->
        <div v-if="task.total_issues > 0" class="text-blue-400">
          $ Issues: {{ task.processed_issues }} / {{ task.total_issues }}
        </div>

        <!-- Message -->
        <div class="text-yellow-400">
          $ {{ task.message }}
        </div>

        <!-- Timestamps -->
        <div class="text-gray-500 text-xs space-y-1 mt-4">
          <div>$ Iniciado: {{ formatDate(task.started_at) }}</div>
          <div v-if="task.completed_at">
            $ Completado: {{ formatDate(task.completed_at) }}
          </div>
        </div>

        <!-- Error Display -->
        <div v-if="task.error" class="mt-3 sm:mt-4 bg-red-900/50 border border-red-700 rounded p-2 sm:p-3">
          <div class="text-red-400 font-bold mb-1 text-xs sm:text-sm">$ ERROR:</div>
          <div class="text-red-300 text-[10px] sm:text-xs">{{ task.error }}</div>
        </div>

        <!-- Success Result -->
        <div v-if="task.status === 'completado' && task.result" 
             class="mt-3 sm:mt-4 bg-green-900/50 border border-green-700 rounded p-2 sm:p-3">
          <div class="text-green-400 font-bold mb-1 text-xs sm:text-sm">$ RESULTADO:</div>
          <div class="text-green-300 text-[10px] sm:text-xs space-y-1">
            <div>Total procesados: {{ task.result.synced_issues }}</div>
            <div>Tiempo total: {{ getElapsedTime(task.started_at, task.completed_at) }}</div>
            <div v-if="task.backup_file" class="mt-2 space-y-2">
              <p class="text-cyan-400">$ Backup generado: {{ task.backup_file }}</p>
              <div v-if="task.backup_absolute_path" class="bg-gray-800 p-2 rounded">
                <p class="text-[10px] text-gray-400">Ruta local:</p>
                <p class="text-[10px] font-mono text-gray-300 break-all">{{ task.backup_absolute_path }}</p>
              </div>
              <div v-if="task.backup_path" class="bg-gray-800 p-2 rounded">
                <p class="text-[10px] text-gray-400">Ruta en contenedor:</p>
                <p class="text-[10px] font-mono text-gray-300">/app/backups/{{ task.backup_file }}</p>
              </div>
              <div v-if="task.backup_size" class="text-[10px] text-gray-400">
                Tamaño: {{ formatFileSize(task.backup_size) }}
              </div>
              <a 
                :href="getBackupUrl(task.backup_file)" 
                target="_blank"
                class="inline-block mt-2 px-3 py-1 bg-green-600 hover:bg-green-700 text-white text-xs rounded transition-colors"
              >
                📥 Descargar Backup SQL
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Animated Cursor -->
      <div v-if="isPolling && task?.status !== 'completado' && task?.status !== 'error'" 
           class="animate-pulse text-gray-400">
        $ Actualizando<span class="inline-block animate-bounce">...</span>
      </div>
    </div>

    <!-- Console Footer -->
    <div class="flex justify-between items-center mt-4 sm:mt-6 pt-3 sm:pt-4 border-t border-gray-700">
      <div class="text-gray-500 text-[10px] sm:text-xs">
        <span v-if="isPolling">🟢 Conectado</span>
        <span v-else>🔴 Desconectado</span>
      </div>
      <button
        v-if="task && ['completado', 'error'].includes(task.status)"
        @click="$emit('clear')"
        class="px-2 sm:px-3 py-0.5 sm:py-1 bg-gray-800 hover:bg-gray-700 rounded text-[10px] sm:text-xs transition-colors"
      >
        Limpiar Consola
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
import type { SyncTask } from '@/stores/jiraSync'

interface Props {
  task: SyncTask | null
  isPolling: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  clear: []
}>()

const statusLabels: Record<string, string> = {
  iniciando: 'Iniciando sincronización',
  obteniendo_total: 'Obteniendo total de issues',
  conectando_db: 'Conectando a base de datos',
  descargando: 'Descargando issues de Jira',
  preparando_tabla: 'Preparando tabla MySQL',
  sincronizando: 'Sincronizando a base de datos',
  generando_respaldo: 'Generando archivo de respaldo SQL',
  completado: 'Sincronización completada ✓',
  error: 'Error en sincronización ✗'
}

const statusLabel = computed(() => {
  if (!props.task) return ''
  return statusLabels[props.task.status] || props.task.status
})

const statusColorClass = computed(() => {
  if (!props.task) return 'text-gray-400'
  
  const colors: Record<string, string> = {
    iniciando: 'text-blue-400',
    obteniendo_total: 'text-blue-400',
    conectando_db: 'text-indigo-400',
    descargando: 'text-yellow-400',
    preparando_tabla: 'text-purple-400',
    sincronizando: 'text-green-400',
    generando_respaldo: 'text-cyan-400',
    completado: 'text-green-400',
    error: 'text-red-400'
  }
  
  return colors[props.task.status] || 'text-gray-400'
})

const progressBarColor = computed(() => {
  if (!props.task) return 'bg-gray-600'
  
  if (props.task.status === 'error') return 'bg-red-600'
  if (props.task.status === 'completado') return 'bg-green-600'
  if (props.task.progress_percentage < 50) return 'bg-yellow-600'
  return 'bg-green-600'
})

function formatDate(dateString: string): string {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

function getElapsedTime(start: string, end: string | null): string {
  if (!start || !end) return ''
  
  const startTime = new Date(start).getTime()
  const endTime = new Date(end).getTime()
  const elapsed = endTime - startTime
  
  const seconds = Math.floor(elapsed / 1000)
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  
  if (minutes > 0) {
    return `${minutes}m ${remainingSeconds}s`
  }
  return `${seconds}s`
}

const getBackupUrl = (filename: string) => {
  const baseUrl = import.meta.env.PROD ? '/api' : 'http://127.0.0.1:8000'
  return `${baseUrl}/backups/${filename}`
}

const statusMessages = {
  iniciando: 'Inicializando sincronización...',
  obteniendo_total: 'Obteniendo cantidad total de issues...',
  conectando_db: 'Conectando a la base de datos MySQL...',
  descargando: 'Descargando issues de Jira...',
  preparando_tabla: 'Preparando tabla en la base de datos...',
  sincronizando: 'Sincronizando issues a MySQL...',
  generando_respaldo: 'Generando archivo de respaldo SQL...',
  completado: 'Sincronización completada exitosamente',
  error: 'Error durante la sincronización'
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script> 