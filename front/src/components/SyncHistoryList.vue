<template>
  <div class="space-y-3">
    <!-- Empty State -->
    <div v-if="!tasks || tasks.length === 0" 
         class="text-center py-8 text-gray-500">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="mt-2">No hay tareas anteriores</p>
    </div>

    <!-- Task List -->
    <div v-else class="divide-y divide-gray-200">
      <div 
        v-for="task in displayTasks" 
        :key="task.task_id"
        class="py-3 hover:bg-gray-50 rounded px-3 transition-colors"
      >
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <!-- Status Badge -->
            <div class="flex items-center gap-2">
              <span 
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                :class="getStatusBadgeClass(task.status)"
              >
                <span class="w-2 h-2 mr-1 rounded-full" 
                      :class="getStatusDotClass(task.status)"></span>
                {{ getStatusLabel(task.status) }}
              </span>
              <span class="text-sm text-gray-500">
                {{ formatRelativeTime(task.started_at) }}
              </span>
            </div>
            
            <!-- Task Details -->
            <div class="mt-1 text-sm text-gray-700">
              <span v-if="task.total_issues > 0">
                {{ task.processed_issues }}/{{ task.total_issues }} issues
              </span>
              <span v-if="task.error" class="text-red-600 ml-2">
                • Error: {{ task.error }}
              </span>
            </div>
          </div>

          <!-- Progress -->
          <div class="ml-4 text-right">
            <div class="text-sm font-medium text-gray-900">
              {{ task.progress_percentage }}%
            </div>
            <div v-if="task.completed_at" class="text-xs text-gray-500">
              {{ getElapsedTime(task.started_at, task.completed_at) }}
            </div>
          </div>
        </div>

        <!-- Progress Bar -->
        <div class="mt-2 w-full bg-gray-200 rounded-full h-1.5">
          <div 
            class="h-1.5 rounded-full transition-all duration-300"
            :class="getProgressBarClass(task.status)"
            :style="{ width: `${task.progress_percentage}%` }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SyncTask } from '@/stores/jiraSync'

interface Props {
  tasks: SyncTask[]
  limit?: number
}

const props = withDefaults(defineProps<Props>(), {
  limit: 5
})

const displayTasks = computed(() => {
  return props.tasks.slice(0, props.limit)
})

function getStatusLabel(status: string): string {
  const labels: Record<string, string> = {
    iniciando: 'Iniciando',
    obteniendo_total: 'Obteniendo',
    conectando_db: 'Conectando',
    descargando: 'Descargando',
    preparando_tabla: 'Preparando',
    sincronizando: 'Sincronizando',
    completado: 'Completado',
    error: 'Error'
  }
  return labels[status] || status
}

function getStatusBadgeClass(status: string): string {
  const classes: Record<string, string> = {
    completado: 'bg-green-100 text-green-800',
    error: 'bg-red-100 text-red-800',
    default: 'bg-blue-100 text-blue-800'
  }
  
  if (status === 'completado') return classes.completado
  if (status === 'error') return classes.error
  return classes.default
}

function getStatusDotClass(status: string): string {
  const classes: Record<string, string> = {
    completado: 'bg-green-400',
    error: 'bg-red-400',
    default: 'bg-blue-400'
  }
  
  if (status === 'completado') return classes.completado
  if (status === 'error') return classes.error
  return classes.default
}

function getProgressBarClass(status: string): string {
  const classes: Record<string, string> = {
    completado: 'bg-green-600',
    error: 'bg-red-600',
    default: 'bg-blue-600'
  }
  
  if (status === 'completado') return classes.completado
  if (status === 'error') return classes.error
  return classes.default
}

function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return 'Hace un momento'
  if (minutes < 60) return `Hace ${minutes}m`
  if (hours < 24) return `Hace ${hours}h`
  if (days < 7) return `Hace ${days}d`
  
  return date.toLocaleDateString('es-ES')
}

function getElapsedTime(start: string, end: string): string {
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
</script> 