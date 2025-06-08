<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <!-- Import/Export JSON buttons and Auto-save toggle -->
    <div class="flex flex-wrap justify-between items-center gap-2 mb-4">
      <!-- Auto-save toggle -->
      <div class="flex items-center gap-2">
        <input
          id="autoSave"
          v-model="autoSaveEnabled"
          type="checkbox"
          class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          @change="handleAutoSaveToggle"
        >
        <label for="autoSave" class="text-xs sm:text-sm text-gray-700">
          Guardar configuración automáticamente
        </label>
      </div>
      
      <!-- Import/Export buttons -->
      <div class="flex flex-wrap gap-2">
      <button
        type="button"
        @click="togglePasteModal"
        :disabled="disabled"
        class="px-2 sm:px-4 py-1.5 sm:py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50 flex items-center gap-1 sm:gap-2 text-xs sm:text-sm"
      >
        <svg class="h-4 sm:h-5 w-4 sm:w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span class="hidden sm:inline">Pegar JSON</span>
        <span class="sm:hidden">Pegar</span>
      </button>
      <button
        type="button"
        @click="importConfig"
        :disabled="disabled"
        class="px-2 sm:px-4 py-1.5 sm:py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center gap-1 sm:gap-2 text-xs sm:text-sm"
      >
        <svg class="h-4 sm:h-5 w-4 sm:w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <span class="hidden sm:inline">Importar Archivo</span>
        <span class="sm:hidden">Importar</span>
      </button>
      <button
        type="button"
        @click="exportConfig"
        :disabled="disabled"
        class="px-2 sm:px-4 py-1.5 sm:py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 flex items-center gap-1 sm:gap-2 text-xs sm:text-sm"
      >
        <svg class="h-4 sm:h-5 w-4 sm:w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        <span class="hidden sm:inline">Exportar JSON</span>
        <span class="sm:hidden">Exportar</span>
      </button>
      </div>
    </div>

    <!-- Paste JSON Modal -->
    <div v-if="showPasteModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Pegar Configuración JSON</h3>
        
        <textarea
          v-model="pastedJson"
          class="w-full h-64 p-3 border border-gray-300 rounded-md font-mono text-sm"
          placeholder="Pega aquí tu configuración JSON..."
        ></textarea>
        
        <div class="mt-4 flex justify-end gap-2">
          <button
            type="button"
            @click="togglePasteModal"
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            type="button"
            @click="importPastedJson"
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Importar
          </button>
        </div>
      </div>
    </div>

    <!-- Jira Configuration -->
    <div class="border-b border-gray-200 pb-4 sm:pb-6">
      <h3 class="text-base sm:text-lg font-medium text-gray-900 mb-3 sm:mb-4">Configuración de Jira</h3>
      
      <div class="grid grid-cols-1 gap-3 sm:gap-4">
        <div>
          <label class="block text-xs sm:text-sm font-medium text-gray-700">Dominio de Jira</label>
          <input
            v-model="formData.jira_domain"
            type="text"
            required
            :disabled="disabled"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-xs sm:text-sm"
            placeholder="your-domain.atlassian.net"
          >
        </div>

        <div>
          <label class="block text-xs sm:text-sm font-medium text-gray-700">Email</label>
          <input
            v-model="formData.jira_email"
            type="email"
            required
            :disabled="disabled"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="tu-email@ejemplo.com"
          >
        </div>

        <div>
          <label class="block text-xs sm:text-sm font-medium text-gray-700">API Token</label>
          <input
            v-model="formData.jira_api_token"
            type="password"
            required
            :disabled="disabled"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="Tu token de API de Jira"
          >
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">JQL Query</label>
          <textarea
            v-model="formData.jql"
            required
            :disabled="disabled"
            rows="2"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="project = SAC AND updated >= -7d"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- Field Mapping -->
    <div class="border-b border-gray-200 pb-4 sm:pb-6">
      <h3 class="text-base sm:text-lg font-medium text-gray-900 mb-3 sm:mb-4">Mapeo de Campos</h3>
      
      <div class="space-y-3">
        <div v-for="(dbField, jiraField) in formData.fields" :key="jiraField" 
             class="flex items-center gap-2">
          <input
            :value="jiraField"
            :disabled="disabled"
            class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="Campo Jira"
            readonly
          >
          <span class="text-gray-500">→</span>
          <input
            v-model="formData.fields[jiraField]"
            :disabled="disabled"
            class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="Campo MySQL"
          >
          <button
            type="button"
            @click="removeField(jiraField)"
            :disabled="disabled"
            class="text-red-600 hover:text-red-800 disabled:opacity-50"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <div class="mt-4 flex items-center gap-2">
        <input
          v-model="newField.jira"
          :disabled="disabled"
          class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="Nuevo campo Jira"
          @keyup.enter="addField"
        >
        <span class="text-gray-500">→</span>
        <input
          v-model="newField.db"
          :disabled="disabled"
          class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="Nombre en MySQL"
          @keyup.enter="addField"
        >
        <button
          type="button"
          @click="addField"
          :disabled="disabled || !newField.jira || !newField.db"
          class="px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
        </button>
      </div>
    </div>

    <!-- MySQL Configuration -->
    <div class="border-b border-gray-200 pb-4 sm:pb-6">
      <h3 class="text-base sm:text-lg font-medium text-gray-900 mb-3 sm:mb-4">Configuración de MySQL</h3>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
        <div>
          <label class="block text-xs sm:text-sm font-medium text-gray-700">Host</label>
          <input
            v-model="formData.mysql_host"
            type="text"
            required
            :disabled="disabled"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Puerto</label>
          <input
            v-model.number="formData.mysql_port"
            type="number"
            required
            :disabled="disabled"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Usuario</label>
          <input
            v-model="formData.mysql_user"
            type="text"
            required
            :disabled="disabled"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Contraseña</label>
          <input
            v-model="formData.mysql_password"
            type="password"
            :disabled="disabled"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Base de Datos</label>
          <input
            v-model="formData.mysql_database"
            type="text"
            required
            :disabled="disabled"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Tabla</label>
          <input
            v-model="formData.mysql_table"
            type="text"
            required
            :disabled="disabled"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
        </div>
      </div>
    </div>

    <!-- Submit Button -->
    <div class="flex justify-end mt-4 sm:mt-6">
      <button
        type="submit"
        :disabled="disabled"
        class="px-4 sm:px-6 py-2 sm:py-3 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm sm:text-base"
      >
        {{ disabled ? 'Sincronización en progreso...' : 'Iniciar Sincronización' }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, toRaw, watch, onMounted } from 'vue'
import { useJiraSyncStore } from '@/stores/jiraSync'
import type { JiraSyncConfig } from '@/stores/jiraSync'

interface Props {
  disabled?: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  submit: [config: JiraSyncConfig]
}>()

const syncStore = useJiraSyncStore()

// Deep copy the default config to avoid reactivity issues
const defaultConfigCopy = JSON.parse(JSON.stringify(toRaw(syncStore.defaultConfig)))

// Ensure fields is always an object
if (!defaultConfigCopy.fields || typeof defaultConfigCopy.fields !== 'object') {
  defaultConfigCopy.fields = {}
}

const formData = reactive<JiraSyncConfig>(defaultConfigCopy)

const newField = reactive({
  jira: '',
  db: ''
})

const showPasteModal = ref(false)
const pastedJson = ref('')

// LocalStorage keys
const CONFIG_STORAGE_KEY = 'jira-sync-config'
const AUTO_SAVE_KEY = 'jira-sync-auto-save'

// Auto-save state (default true)
const autoSaveEnabled = ref(true)

function addField() {
  if (newField.jira && newField.db) {
    // Ensure fields exists before adding
    if (!formData.fields) {
      formData.fields = {}
    }
    formData.fields[newField.jira] = newField.db
    newField.jira = ''
    newField.db = ''
  }
}

function removeField(jiraField: string) {
  if (formData.fields && jiraField in formData.fields) {
    delete formData.fields[jiraField]
  }
}

function handleSubmit() {
  // Ensure fields is not empty
  if (!formData.fields || Object.keys(formData.fields).length === 0) {
    alert('Por favor, agrega al menos un campo para mapear')
    return
  }
  emit('submit', { ...formData })
}

function importConfig() {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json'
  
  input.onchange = async (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0]
    if (!file) return
    
    try {
      const text = await file.text()
      const config = JSON.parse(text) as JiraSyncConfig
      
      // Validate the imported config has required fields
      if (!config.jira_domain || !config.jira_email || !config.jira_api_token || !config.jql) {
        alert('El archivo JSON no contiene todos los campos requeridos de Jira')
        return
      }
      
      if (!config.mysql_host || !config.mysql_database || !config.mysql_table) {
        alert('El archivo JSON no contiene todos los campos requeridos de MySQL')
        return
      }
      
      // Update form data with imported config
      Object.assign(formData, config)
      
      // Save to localStorage if enabled
      if (autoSaveEnabled.value) {
        saveToLocalStorage()
      }
      
      alert('Configuración importada exitosamente')
    } catch (error) {
      alert('Error al importar el archivo: ' + (error as Error).message)
    }
  }
  
  input.click()
}

function exportConfig() {
  try {
    // Create a clean copy of the config
    const configToExport = {
      jira_domain: formData.jira_domain,
      jira_email: formData.jira_email,
      jira_api_token: formData.jira_api_token,
      jql: formData.jql,
      fields: { ...formData.fields },
      mysql_host: formData.mysql_host,
      mysql_port: formData.mysql_port,
      mysql_user: formData.mysql_user,
      mysql_password: formData.mysql_password,
      mysql_database: formData.mysql_database,
      mysql_table: formData.mysql_table,
      max_results_per_page: formData.max_results_per_page || 50
    }
    
    // Create blob and download
    const blob = new Blob([JSON.stringify(configToExport, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `jira-sync-config-${new Date().toISOString().split('T')[0]}.json`
    link.click()
    
    URL.revokeObjectURL(url)
  } catch (error) {
    alert('Error al exportar la configuración: ' + (error as Error).message)
  }
}

function togglePasteModal() {
  showPasteModal.value = !showPasteModal.value
  if (showPasteModal.value) {
    pastedJson.value = ''
  }
}

function importPastedJson() {
  try {
    const config = JSON.parse(pastedJson.value) as JiraSyncConfig
    
    // Validate the imported config has required fields
    if (!config.jira_domain || !config.jira_email || !config.jira_api_token || !config.jql) {
      alert('El JSON no contiene todos los campos requeridos de Jira')
      return
    }
    
    if (!config.mysql_host || !config.mysql_database || !config.mysql_table) {
      alert('El JSON no contiene todos los campos requeridos de MySQL')
      return
    }
    
    // Update form data with imported config
    Object.assign(formData, config)
    
    // Save to localStorage if enabled
    if (autoSaveEnabled.value) {
      saveToLocalStorage()
    }
    
    // Close modal
    togglePasteModal()
    
    alert('Configuración importada exitosamente')
  } catch (error) {
    alert('Error al parsear el JSON: ' + (error as Error).message)
  }
}

// LocalStorage functions
function saveToLocalStorage() {
  if (autoSaveEnabled.value) {
    try {
      const configToSave = {
        jira_domain: formData.jira_domain,
        jira_email: formData.jira_email,
        jira_api_token: formData.jira_api_token,
        jql: formData.jql,
        fields: { ...formData.fields },
        mysql_host: formData.mysql_host,
        mysql_port: formData.mysql_port,
        mysql_user: formData.mysql_user,
        mysql_password: formData.mysql_password,
        mysql_database: formData.mysql_database,
        mysql_table: formData.mysql_table,
        max_results_per_page: formData.max_results_per_page || 50
      }
      localStorage.setItem(CONFIG_STORAGE_KEY, JSON.stringify(configToSave))
    } catch (error) {
      console.error('Error saving to localStorage:', error)
    }
  }
}

function loadFromLocalStorage() {
  try {
    // Load auto-save preference
    const savedAutoSave = localStorage.getItem(AUTO_SAVE_KEY)
    if (savedAutoSave !== null) {
      autoSaveEnabled.value = savedAutoSave === 'true'
    }
    
    // Load config if auto-save is enabled
    if (autoSaveEnabled.value) {
      const savedConfig = localStorage.getItem(CONFIG_STORAGE_KEY)
      if (savedConfig) {
        const config = JSON.parse(savedConfig) as JiraSyncConfig
        Object.assign(formData, config)
      }
    }
  } catch (error) {
    console.error('Error loading from localStorage:', error)
  }
}

function handleAutoSaveToggle() {
  localStorage.setItem(AUTO_SAVE_KEY, String(autoSaveEnabled.value))
  if (autoSaveEnabled.value) {
    saveToLocalStorage()
  } else {
    // Optionally clear saved config when disabling auto-save
    // localStorage.removeItem(CONFIG_STORAGE_KEY)
  }
}

// Watch for changes and auto-save
watch(
  () => ({ ...formData }),
  () => {
    if (autoSaveEnabled.value) {
      saveToLocalStorage()
    }
  },
  { deep: true }
)

// Load saved config on mount
onMounted(() => {
  loadFromLocalStorage()
})
</script> 