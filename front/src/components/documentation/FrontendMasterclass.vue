<template>
  <div class="space-y-8">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">🎨 Frontend Development Masterclass</h2>
    
    <!-- Introducción -->
    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-3">🚀 Bienvenido al Frontend de Jira-MySQL Sync</h3>
      <p class="text-gray-700 mb-4">
        Esta masterclass te enseñará cómo está construido el frontend, cómo funciona cada componente, 
        y cómo puedes extender la aplicación con nuevas funcionalidades. Al final, serás capaz de:
      </p>
      <ul class="list-disc list-inside space-y-1 text-gray-700">
        <li>Entender la arquitectura Vue 3 con Composition API</li>
        <li>Manejar el estado global con Pinia</li>
        <li>Crear nuevos componentes siguiendo los patrones establecidos</li>
        <li>Integrar nuevos endpoints del backend</li>
        <li>Implementar nuevas funcionalidades end-to-end</li>
      </ul>
    </div>

    <!-- Arquitectura General -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">📐 Arquitectura del Frontend</h3>
      
      <div class="bg-gray-50 rounded-lg p-6 mb-4">
        <h4 class="font-semibold text-gray-900 mb-3">Stack Tecnológico</h4>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white rounded p-4 border border-gray-200">
            <h5 class="font-semibold text-indigo-600 mb-2">Core Framework</h5>
            <ul class="text-sm space-y-1">
              <li>✅ Vue 3.4+ (Composition API)</li>
              <li>✅ TypeScript 5.0+</li>
              <li>✅ Vite 5.0+ (Build tool)</li>
            </ul>
          </div>
          <div class="bg-white rounded p-4 border border-gray-200">
            <h5 class="font-semibold text-green-600 mb-2">State & Routing</h5>
            <ul class="text-sm space-y-1">
              <li>✅ Pinia (State Management)</li>
              <li>✅ Vue Router 4</li>
              <li>✅ Axios (HTTP Client)</li>
            </ul>
          </div>
          <div class="bg-white rounded p-4 border border-gray-200">
            <h5 class="font-semibold text-purple-600 mb-2">UI & Styling</h5>
            <ul class="text-sm space-y-1">
              <li>✅ Tailwind CSS 3.3</li>
              <li>✅ Heroicons</li>
              <li>✅ Custom Animations</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="bg-gray-50 rounded-lg p-6">
        <h4 class="font-semibold text-gray-900 mb-3">Estructura de Carpetas</h4>
        <pre class="text-sm bg-gray-900 text-gray-100 p-4 rounded overflow-x-auto"><code>front/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── JiraSyncForm.vue      # Formulario principal
│   │   ├── SyncProgressConsole.vue # Consola de progreso
│   │   ├── SyncHistoryList.vue   # Lista de historial
│   │   ├── SyncLogsViewer.vue    # Visor de logs
│   │   └── SyncDetailModal.vue   # Modal de detalles
│   │
│   ├── views/              # Páginas/Vistas principales
│   │   ├── HomeView.vue         # Página de inicio
│   │   ├── JiraSyncView.vue     # Vista principal de sync
│   │   ├── AboutView.vue        # Página sobre nosotros
│   │   └── DocumentationView.vue # Esta documentación
│   │
│   ├── stores/             # Estado global (Pinia)
│   │   └── jiraSync.ts          # Store principal
│   │
│   ├── router/             # Configuración de rutas
│   │   └── index.ts
│   │
│   ├── assets/             # Recursos estáticos
│   ├── App.vue             # Componente raíz
│   └── main.ts             # Punto de entrada</code></pre>
      </div>
    </div>

    <!-- Estado Global con Pinia -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🗃️ Estado Global con Pinia</h3>
      
      <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
        <p class="text-sm text-yellow-700">
          <strong>💡 Concepto Clave:</strong> Pinia es el store management oficial de Vue 3. 
          Piensa en él como una base de datos en memoria que todos los componentes pueden acceder y modificar.
        </p>
      </div>

      <div class="space-y-4">
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">El Store Principal: jiraSync.ts</h4>
          
          <div class="bg-gray-50 rounded p-4 mb-3">
            <p class="text-sm font-semibold mb-2">1. Definición del Store</p>
            <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useJiraSyncStore = defineStore('jiraSync', () => {
  // State reactivo
  const currentTask = ref&lt;SyncTask | null&gt;(null)
  const isPolling = ref(false)
  const syncHistory = ref&lt;SyncTask[]&gt;([])
  
  // Computed properties
  const isRunning = computed(() => {
    return currentTask.value && 
           !['completado', 'error'].includes(currentTask.value.status)
  })
  
  // Actions
  async function startSync(config: JiraSyncConfig) {
    // Lógica de sincronización
  }
  
  return {
    // Exponer todo lo que los componentes necesitan
    currentTask,
    isPolling,
    syncHistory,
    isRunning,
    startSync
  }
})</code></pre>
          </div>

          <div class="bg-gray-50 rounded p-4 mb-3">
            <p class="text-sm font-semibold mb-2">2. Usar el Store en un Componente</p>
            <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>&lt;script setup lang="ts"&gt;
import { useJiraSyncStore } from '@/stores/jiraSync'

// Obtener instancia del store
const store = useJiraSyncStore()

// Acceder a estado reactivo
console.log(store.currentTask)
console.log(store.isRunning)

// Llamar acciones
async function handleSync() {
  await store.startSync(config)
}
&lt;/script&gt;</code></pre>
          </div>

          <div class="bg-blue-50 rounded p-4">
            <p class="text-sm font-semibold text-blue-700 mb-2">🎯 Mejores Prácticas:</p>
            <ul class="text-sm space-y-1 list-disc list-inside">
              <li>Mantén el store enfocado en un dominio específico</li>
              <li>Usa <code class="bg-white px-1 rounded">computed</code> para valores derivados</li>
              <li>Las acciones async deben manejar errores internamente</li>
              <li>Evita mutar el estado directamente fuera de las acciones</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Componentes Principales -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🧩 Componentes Principales Explicados</h3>
      
      <!-- JiraSyncForm -->
      <div class="border rounded-lg p-6 mb-6">
        <h4 class="text-lg font-semibold text-gray-900 mb-3">1. JiraSyncForm.vue - El Cerebro de la Configuración</h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div class="bg-gray-50 rounded p-4">
            <p class="text-sm font-semibold mb-2">🎯 Propósito:</p>
            <p class="text-sm text-gray-700">
              Captura y valida toda la configuración necesaria para sincronizar Jira con MySQL.
              Maneja autenticación, queries JQL, mapeo de campos y configuración de base de datos.
            </p>
          </div>
          <div class="bg-gray-50 rounded p-4">
            <p class="text-sm font-semibold mb-2">📋 Responsabilidades:</p>
            <ul class="text-sm text-gray-700 space-y-1 list-disc list-inside">
              <li>Validación de formularios en tiempo real</li>
              <li>Persistencia en localStorage</li>
              <li>Import/Export de configuraciones</li>
              <li>Mapeo dinámico de campos</li>
            </ul>
          </div>
        </div>

        <div class="bg-gray-50 rounded p-4 mb-3">
          <p class="text-sm font-semibold mb-2">Implementación Clave - Validación Reactiva:</p>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>&lt;script setup lang="ts"&gt;
import { ref, computed, watch } from 'vue'

// Props
const props = defineProps&lt;{
  disabled?: boolean
}&gt;()

// Emits
const emit = defineEmits&lt;{
  submit: [config: JiraSyncConfig]
}&gt;()

// Estado del formulario
const formData = ref({
  jira_domain: '',
  jira_email: '',
  jira_api_token: '',
  jql: '',
  // ... más campos
})

// Validación reactiva
const isFormValid = computed(() => {
  return formData.value.jira_domain.trim() !== '' &&
         formData.value.jira_email.includes('@') &&
         formData.value.jira_api_token.length > 10 &&
         formData.value.jql.trim() !== ''
})

// Auto-guardado en localStorage
watch(formData, (newData) => {
  localStorage.setItem('jiraSyncConfig', JSON.stringify(newData))
}, { deep: true })

// Submit handler
function handleSubmit() {
  if (isFormValid.value && !props.disabled) {
    emit('submit', formData.value)
  }
}
&lt;/script&gt;</code></pre>
        </div>

        <div class="bg-green-50 rounded p-4">
          <p class="text-sm font-semibold text-green-700 mb-2">✨ Características Avanzadas:</p>
          <ul class="text-sm space-y-1 list-disc list-inside">
            <li><strong>Import JSON:</strong> Carga configuraciones desde archivo</li>
            <li><strong>Export JSON:</strong> Guarda configuración con timestamp</li>
            <li><strong>Field Mapping:</strong> UI dinámica para mapear campos Jira → MySQL</li>
            <li><strong>Test Connection:</strong> Valida credenciales antes de sincronizar</li>
          </ul>
        </div>
      </div>

      <!-- SyncProgressConsole -->
      <div class="border rounded-lg p-6 mb-6">
        <h4 class="text-lg font-semibold text-gray-900 mb-3">2. SyncProgressConsole.vue - Feedback Visual en Tiempo Real</h4>
        
        <div class="bg-gray-50 rounded p-4 mb-3">
          <p class="text-sm font-semibold mb-2">Implementación de la Consola:</p>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>&lt;template&gt;
  &lt;div class="bg-gray-900 rounded-lg p-4 h-96 overflow-y-auto font-mono text-sm"&gt;
    &lt;div v-for="(line, index) in consoleLines" :key="index"&gt;
      &lt;span :class="getLineColor(line)"&gt;&#123;&#123; line.text &#125;&#125;&lt;/span&gt;
    &lt;/div&gt;
    
    &lt;!-- Progress Bar --&gt;
    &lt;div v-if="task?.progress_percentage" class="mt-4"&gt;
      &lt;div class="bg-gray-700 rounded-full h-2"&gt;
        &lt;div 
          class="bg-green-500 h-2 rounded-full transition-all duration-500"
          :style="&#123; width: `${task.progress_percentage}%` &#125;"
        &gt;&lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps&lt;{
  task: SyncTask | null
  isPolling: boolean
}&gt;()

// Generar líneas de consola basadas en el estado
const consoleLines = computed(() => {
  const lines = []
  
  if (!props.task) {
    lines.push({ text: '$ Esperando inicio de sincronización...', type: 'info' })
    return lines
  }
  
  // Agregar líneas según el estado
  lines.push({ text: `$ Iniciando sincronización [${props.task.task_id}]`, type: 'info' })
  
  if (props.task.total_issues > 0) {
    lines.push({ 
      text: `✓ Total de issues encontrados: ${props.task.total_issues}`, 
      type: 'success' 
    })
  }
  
  // ... más lógica de líneas
  
  return lines
})

// Auto-scroll al final
const consoleRef = ref&lt;HTMLElement&gt;()
watch(consoleLines, async () => {
  await nextTick()
  if (consoleRef.value) {
    consoleRef.value.scrollTop = consoleRef.value.scrollHeight
  }
})
&lt;/script&gt;</code></pre>
        </div>

        <div class="bg-purple-50 rounded p-4">
          <p class="text-sm font-semibold text-purple-700 mb-2">🎨 Técnicas de UX:</p>
          <ul class="text-sm space-y-1 list-disc list-inside">
            <li>Animación tipo "typewriter" para nuevas líneas</li>
            <li>Colores semánticos (verde=éxito, amarillo=progreso, rojo=error)</li>
            <li>Auto-scroll suave para seguir el progreso</li>
            <li>Barra de progreso animada con transiciones CSS</li>
          </ul>
        </div>
      </div>

      <!-- SyncHistoryList -->
      <div class="border rounded-lg p-6">
        <h4 class="text-lg font-semibold text-gray-900 mb-3">3. SyncHistoryList.vue - Historial Inteligente</h4>
        
        <div class="bg-gray-50 rounded p-4 mb-3">
          <p class="text-sm font-semibold mb-2">Patrón de Lista Reactiva:</p>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>&lt;script setup lang="ts"&gt;
// Mostrar las últimas 5 sincronizaciones
const recentTasks = computed(() => {
  return props.tasks
    .slice(0, 5)
    .map(task => ({
      ...task,
      // Agregar propiedades computadas
      duration: calculateDuration(task.started_at, task.completed_at),
      statusIcon: getStatusIcon(task.status),
      statusColor: getStatusColor(task.status)
    }))
})

// Formato de duración legible
function calculateDuration(start: string, end: string | null): string {
  if (!end) return 'En progreso...'
  
  const duration = new Date(end).getTime() - new Date(start).getTime()
  const seconds = Math.floor(duration / 1000)
  
  if (seconds < 60) return `${seconds}s`
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`
  return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`
}
&lt;/script&gt;</code></pre>
        </div>
      </div>
    </div>

    <!-- Patrones de Desarrollo -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🎯 Patrones de Desarrollo y Mejores Prácticas</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">Composables Personalizados</h4>
          <p class="text-sm text-gray-700 mb-3">
            Crea funciones reutilizables para lógica común:
          </p>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>// composables/useLocalStorage.ts
import { ref, watch, Ref } from 'vue'

export function useLocalStorage&lt;T&gt;(
  key: string, 
  defaultValue: T
): [Ref&lt;T&gt;, () => void] {
  const data = ref&lt;T&gt;(defaultValue)
  
  // Cargar del localStorage
  const stored = localStorage.getItem(key)
  if (stored) {
    try {
      data.value = JSON.parse(stored)
    } catch (e) {
      console.error('Error parsing stored data:', e)
    }
  }
  
  // Auto-guardar cambios
  watch(data, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue))
  }, { deep: true })
  
  // Función para limpiar
  const clear = () => {
    localStorage.removeItem(key)
    data.value = defaultValue
  }
  
  return [data, clear]
}</code></pre>
        </div>

        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">Manejo de Errores Global</h4>
          <p class="text-sm text-gray-700 mb-3">
            Implementa un sistema consistente de errores:
          </p>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>// composables/useErrorHandler.ts
import { ref } from 'vue'

export function useErrorHandler() {
  const error = ref&lt;string | null&gt;(null)
  const isLoading = ref(false)
  
  async function handleAsync&lt;T&gt;(
    fn: () => Promise&lt;T&gt;
  ): Promise&lt;T | null&gt; {
    error.value = null
    isLoading.value = true
    
    try {
      const result = await fn()
      return result
    } catch (e: any) {
      error.value = e.message || 'Error desconocido'
      console.error('Error handled:', e)
      return null
    } finally {
      isLoading.value = false
    }
  }
  
  return {
    error,
    isLoading,
    handleAsync
  }
}</code></pre>
        </div>
      </div>
    </div>

    <!-- Integración con el Backend -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🔌 Integración con el Backend</h3>
      
      <div class="bg-indigo-50 rounded-lg p-6">
        <h4 class="font-semibold text-gray-900 mb-3">Configuración de Axios</h4>
        <pre class="text-sm bg-gray-900 text-gray-100 p-4 rounded overflow-x-auto"><code>// services/api.ts
import axios from 'axios'

// Crear instancia de axios con configuración base
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para manejar errores globalmente
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Manejar no autorizado
      console.error('Unauthorized access')
    } else if (error.response?.status === 500) {
      // Error del servidor
      console.error('Server error:', error.response.data)
    }
    return Promise.reject(error)
  }
)

// Servicios específicos
export const jiraService = {
  async startSync(config: JiraSyncConfig) {
    const response = await api.post('/sync-jira-issues', config)
    return response.data
  },
  
  async getStatus(taskId: string) {
    const response = await api.get(`/sync-status/${taskId}`)
    return response.data
  },
  
  async getLogs(limit = 10, offset = 0) {
    const response = await api.get('/api/logs/all', {
      params: { limit, offset }
    })
    return response.data
  }
}

export default api</code></pre>
      </div>
    </div>

    <!-- Añadir Nueva Funcionalidad -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🚀 Cómo Añadir una Nueva Funcionalidad</h3>
      
      <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-6">
        <h4 class="font-semibold text-gray-900 mb-4">Ejemplo Práctico: Añadir "Programación de Sincronizaciones"</h4>
        
        <div class="space-y-4">
          <div class="bg-white rounded p-4 border border-green-200">
            <p class="font-semibold text-green-700 mb-2">Paso 1: Actualizar el Store</p>
            <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>// En jiraSync.ts, añadir:
interface ScheduledSync {
  id: string
  config: JiraSyncConfig
  schedule: string // Cron expression
  enabled: boolean
  lastRun?: string
  nextRun?: string
}

// Nuevo estado
const scheduledSyncs = ref&lt;ScheduledSync[]&gt;([])

// Nuevas acciones
async function createSchedule(schedule: ScheduledSync) {
  const response = await api.post('/schedules', schedule)
  scheduledSyncs.value.push(response.data)
  return response.data
}

async function toggleSchedule(id: string) {
  const schedule = scheduledSyncs.value.find(s => s.id === id)
  if (schedule) {
    schedule.enabled = !schedule.enabled
    await api.patch(`/schedules/${id}`, { enabled: schedule.enabled })
  }
}</code></pre>
          </div>

          <div class="bg-white rounded p-4 border border-green-200">
            <p class="font-semibold text-green-700 mb-2">Paso 2: Crear el Componente</p>
            <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>// components/ScheduleManager.vue
&lt;template&gt;
  &lt;div class="bg-white rounded-lg shadow p-6"&gt;
    &lt;h3 class="text-lg font-semibold mb-4"&gt;
      📅 Sincronizaciones Programadas
    &lt;/h3&gt;
    
    &lt;!-- Lista de schedules --&gt;
    &lt;div class="space-y-3"&gt;
      &lt;div 
        v-for="schedule in schedules" 
        :key="schedule.id"
        class="border rounded p-4 flex items-center justify-between"
      &gt;
        &lt;div&gt;
          &lt;p class="font-medium"&gt;&#123;&#123; schedule.config.jql &#125;&#125;&lt;/p&gt;
          &lt;p class="text-sm text-gray-600"&gt;
            Próxima ejecución: &#123;&#123; formatDate(schedule.nextRun) &#125;&#125;
          &lt;/p&gt;
        &lt;/div&gt;
        
        &lt;button
          @click="toggleSchedule(schedule.id)"
          :class="[
            'px-4 py-2 rounded transition-colors',
            schedule.enabled 
              ? 'bg-green-100 text-green-700 hover:bg-green-200'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          ]"
        &gt;
          &#123;&#123; schedule.enabled ? 'Activo' : 'Inactivo' &#125;&#125;
        &lt;/button&gt;
      &lt;/div&gt;
    &lt;/div&gt;
    
    &lt;!-- Botón para añadir --&gt;
    &lt;button 
      @click="showAddModal = true"
      class="mt-4 w-full py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
    &gt;
      + Añadir Programación
    &lt;/button&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref, onMounted } from 'vue'
import { useJiraSyncStore } from '@/stores/jiraSync'

const store = useJiraSyncStore()
const schedules = ref&lt;ScheduledSync[]&gt;([])
const showAddModal = ref(false)

onMounted(async () => {
  schedules.value = await store.loadSchedules()
})

async function toggleSchedule(id: string) {
  await store.toggleSchedule(id)
}
&lt;/script&gt;</code></pre>
          </div>

          <div class="bg-white rounded p-4 border border-green-200">
            <p class="font-semibold text-green-700 mb-2">Paso 3: Integrar en la Vista Principal</p>
            <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>// En JiraSyncView.vue, importar y usar:
&lt;template&gt;
  &lt;div class="grid grid-cols-1 lg:grid-cols-2 gap-6"&gt;
    &lt;!-- Columna existente --&gt;
    &lt;div&gt;
      &lt;JiraSyncForm /&gt;
      &lt;SyncHistoryList /&gt;
    &lt;/div&gt;
    
    &lt;!-- Nueva columna --&gt;
    &lt;div&gt;
      &lt;SyncProgressConsole /&gt;
      &lt;ScheduleManager class="mt-6" /&gt; &lt;!-- Nuevo componente --&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;</code></pre>
          </div>
        </div>
      </div>
    </div>

    <!-- Testing y Debugging -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">🧪 Testing y Debugging</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">Vue DevTools</h4>
          <p class="text-sm text-gray-700 mb-2">Herramientas esenciales para debugging:</p>
          <ul class="text-sm space-y-1 list-disc list-inside">
            <li>Inspeccionar componentes y sus props</li>
            <li>Ver el estado de Pinia en tiempo real</li>
            <li>Timeline de eventos y renders</li>
            <li>Performance profiling</li>
          </ul>
        </div>
        
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">Testing con Vitest</h4>
          <pre class="text-sm bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>// tests/JiraSyncForm.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import JiraSyncForm from '@/components/JiraSyncForm.vue'

describe('JiraSyncForm', () => {
  it('validates email format', async () => {
    const wrapper = mount(JiraSyncForm)
    
    const emailInput = wrapper.find('[data-test="email-input"]')
    await emailInput.setValue('invalid-email')
    
    expect(wrapper.find('.error-message').exists()).toBe(true)
  })
  
  it('emits submit event with valid data', async () => {
    const wrapper = mount(JiraSyncForm)
    
    // Llenar formulario
    await wrapper.find('[data-test="domain-input"]').setValue('test.atlassian.net')
    await wrapper.find('[data-test="email-input"]').setValue('test@example.com')
    // ... más campos
    
    await wrapper.find('form').trigger('submit')
    
    expect(wrapper.emitted('submit')).toBeTruthy()
    expect(wrapper.emitted('submit')[0][0]).toMatchObject({
      jira_domain: 'test.atlassian.net',
      jira_email: 'test@example.com'
    })
  })
})</code></pre>
        </div>
      </div>
    </div>

    <!-- Recursos y Siguiente Paso -->
    <div class="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">📚 Recursos y Siguientes Pasos</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h4 class="font-semibold text-gray-900 mb-2">Documentación Oficial</h4>
          <ul class="text-sm space-y-1">
            <li>📖 <a href="https://vuejs.org/" class="text-indigo-600 hover:underline" target="_blank">Vue 3 Documentation</a></li>
            <li>📖 <a href="https://pinia.vuejs.org/" class="text-indigo-600 hover:underline" target="_blank">Pinia Documentation</a></li>
            <li>📖 <a href="https://tailwindcss.com/" class="text-indigo-600 hover:underline" target="_blank">Tailwind CSS</a></li>
            <li>📖 <a href="https://www.typescriptlang.org/" class="text-indigo-600 hover:underline" target="_blank">TypeScript Handbook</a></li>
          </ul>
        </div>
        
        <div>
          <h4 class="font-semibold text-gray-900 mb-2">Próximas Funcionalidades Sugeridas</h4>
          <ul class="text-sm space-y-1">
            <li>🚀 Dashboard con métricas y gráficos</li>
            <li>🚀 Notificaciones en tiempo real</li>
            <li>🚀 Multi-idioma (i18n)</li>
            <li>🚀 Modo oscuro</li>
            <li>🚀 PWA support</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Component logic
</script>

<style scoped>
pre code {
  @apply block;
}
</style>
