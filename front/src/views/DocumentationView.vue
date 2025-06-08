<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="bg-white shadow-sm rounded-lg mb-8 p-6">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Documentación Técnica</h1>
        <p class="text-gray-600">Sistema de Sincronización Jira-MySQL v2.0</p>
      </div>

      <!-- Navigation Tabs -->
      <div class="bg-white shadow-sm rounded-lg mb-6">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-4 px-6 overflow-x-auto" aria-label="Tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                activeTab === tab.id
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-2 border-b-2 font-medium text-sm cursor-pointer flex-shrink-0'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Content -->
      <div class="bg-white shadow rounded-lg p-6">
        <component :is="currentComponent" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import VersionHistory from '@/components/documentation/VersionHistory.vue'
import ApiDocumentation from '@/components/documentation/ApiDocumentation.vue'
import ComponentsDocumentation from '@/components/documentation/ComponentsDocumentation.vue'
import ArchitectureDocumentation from '@/components/documentation/ArchitectureDocumentation.vue'
import DockerDocumentation from '@/components/documentation/DockerDocumentation.vue'
import ConfigurationGuide from '@/components/documentation/ConfigurationGuide.vue'
import FrontendMasterclass from '@/components/documentation/FrontendMasterclass.vue'
import BackendMasterclass from '@/components/documentation/BackendMasterclass.vue'

const activeTab = ref('frontend-master')

const tabs = [
  { id: 'frontend-master', name: '🎨 Frontend Dev' },
  { id: 'backend-master', name: '🔧 Backend Dev' },
  { id: 'versions', name: '📝 Versiones' },
  { id: 'api', name: '🔌 API REST' },
  { id: 'components', name: '🧩 Componentes' },
  { id: 'architecture', name: '📐 Arquitectura' },
  { id: 'docker', name: '🐳 Docker' },
  { id: 'config', name: '⚙️ Config' }
]

// Mapeo de tabs a componentes
const componentMap: Record<string, any> = {
  'frontend-master': FrontendMasterclass,
  'backend-master': BackendMasterclass,
  versions: VersionHistory,
  api: ApiDocumentation,
  components: ComponentsDocumentation,
  architecture: ArchitectureDocumentation,
  docker: DockerDocumentation,
  config: ConfigurationGuide
}

// Computed para obtener el componente actual
const currentComponent = computed(() => {
  return componentMap[activeTab.value] || FrontendMasterclass
})
</script>

<style scoped>
/* Estilos para tabs responsivos en móvil */
@media (max-width: 640px) {
  nav {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  nav::-webkit-scrollbar {
    display: none;
  }
}
</style> 