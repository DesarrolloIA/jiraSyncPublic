<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
      <!-- Hero Section -->
      <div class="bg-white rounded-lg shadow-lg overflow-hidden mb-8">
        <div class="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-8 sm:px-8 sm:py-12">
          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4">
            Jira Sync Manager
          </h1>
          <p class="text-xl text-indigo-100 max-w-3xl">
            Sincronización automatizada de issues de Jira Cloud a MySQL con mapeo flexible de campos
          </p>
        </div>
      </div>

      <!-- Features Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <!-- Feature 1 -->
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Importación Flexible</h3>
          <p class="text-gray-600">
            Importa configuraciones desde archivos JSON, pega directamente o usa el guardado automático en localStorage
          </p>
        </div>

        <!-- Feature 2 -->
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Sincronización en Tiempo Real</h3>
          <p class="text-gray-600">
            Monitorea el progreso con una consola interactiva que muestra el estado, porcentaje y mensajes en tiempo real
          </p>
        </div>

        <!-- Feature 3 -->
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Mapeo Personalizable</h3>
          <p class="text-gray-600">
            Define qué campos de Jira se sincronizan y cómo se nombran en MySQL, incluyendo campos personalizados
          </p>
        </div>

        <!-- Feature 4 -->
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Creación Dinámica de Tablas</h3>
          <p class="text-gray-600">
            Crea automáticamente tablas MySQL con tipos de datos apropiados y agrega columnas según sea necesario
          </p>
        </div>

        <!-- Feature 5 -->
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Conexión Segura</h3>
          <p class="text-gray-600">
            Utiliza autenticación API de Jira y conexiones seguras a MySQL con manejo robusto de errores
          </p>
        </div>

        <!-- Feature 6 -->
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Historial de Tareas</h3>
          <p class="text-gray-600">
            Mantén un registro de todas las sincronizaciones realizadas con tiempos, resultados y estadísticas
          </p>
        </div>
      </div>

      <!-- Quick Start Section -->
      <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Inicio Rápido</h2>
        
        <div class="space-y-4">
          <div class="flex items-start">
            <div class="flex-shrink-0 w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center font-semibold">
              1
            </div>
            <div class="ml-4">
              <h3 class="font-semibold text-gray-900">Configura tu conexión a Jira</h3>
              <p class="text-gray-600 mt-1">
                Ingresa tu dominio de Atlassian (ej: tu-empresa.atlassian.net), email y token API
              </p>
            </div>
          </div>

          <div class="flex items-start">
            <div class="flex-shrink-0 w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center font-semibold">
              2
            </div>
            <div class="ml-4">
              <h3 class="font-semibold text-gray-900">Define tu consulta JQL</h3>
              <p class="text-gray-600 mt-1">
                Especifica qué issues deseas sincronizar usando JQL (ej: project = SAC AND updated >= -7d)
              </p>
            </div>
          </div>

          <div class="flex items-start">
            <div class="flex-shrink-0 w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center font-semibold">
              3
            </div>
            <div class="ml-4">
              <h3 class="font-semibold text-gray-900">Mapea los campos</h3>
              <p class="text-gray-600 mt-1">
                Selecciona qué campos de Jira sincronizar y cómo nombrarlos en tu base de datos MySQL
              </p>
            </div>
          </div>

          <div class="flex items-start">
            <div class="flex-shrink-0 w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center font-semibold">
              4
            </div>
            <div class="ml-4">
              <h3 class="font-semibold text-gray-900">Configura MySQL</h3>
              <p class="text-gray-600 mt-1">
                Proporciona los detalles de conexión a tu base de datos MySQL
              </p>
            </div>
          </div>

          <div class="flex items-start">
            <div class="flex-shrink-0 w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center font-semibold">
              5
            </div>
            <div class="ml-4">
              <h3 class="font-semibold text-gray-900">¡Inicia la sincronización!</h3>
              <p class="text-gray-600 mt-1">
                Haz clic en "Iniciar Sincronización" y observa el progreso en tiempo real
              </p>
            </div>
          </div>
        </div>

        <div class="mt-8 flex gap-4">
          <RouterLink 
            to="/jira-sync" 
            class="inline-flex items-center px-6 py-3 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 transition-colors"
          >
            Comenzar Ahora
            <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </RouterLink>
          <RouterLink 
            to="/about" 
            class="inline-flex items-center px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-md hover:bg-gray-50 transition-colors"
          >
            Ver Documentación
          </RouterLink>
        </div>
      </div>

      <!-- Tech Stack -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Stack Tecnológico</h2>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
          <div class="p-3 bg-gray-50 rounded-lg">
            <div class="text-2xl mb-1">⚡</div>
            <div class="text-sm font-medium text-gray-700">FastAPI</div>
          </div>
          <div class="p-3 bg-gray-50 rounded-lg">
            <div class="text-2xl mb-1">🟩</div>
            <div class="text-sm font-medium text-gray-700">Vue 3</div>
          </div>
          <div class="p-3 bg-gray-50 rounded-lg">
            <div class="text-2xl mb-1">🐬</div>
            <div class="text-sm font-medium text-gray-700">MySQL</div>
          </div>
          <div class="p-3 bg-gray-50 rounded-lg">
            <div class="text-2xl mb-1">🔧</div>
            <div class="text-sm font-medium text-gray-700">TypeScript</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
