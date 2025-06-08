<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
      <!-- Header -->
      <div class="bg-white rounded-lg shadow-lg overflow-hidden mb-8">
        <div class="bg-gradient-to-r from-purple-600 to-indigo-600 px-6 py-8">
          <h1 class="text-3xl sm:text-4xl font-bold text-white mb-4">
            Documentación Técnica
          </h1>
          <p class="text-xl text-purple-100">
            Guía completa de implementación y uso de Jira Sync Manager
          </p>
        </div>
      </div>

      <!-- Table of Contents -->
      <div class="bg-white rounded-lg shadow p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Tabla de Contenidos</h2>
        <nav class="space-y-2">
          <a href="#arquitectura" class="block text-indigo-600 hover:text-indigo-800">1. Arquitectura del Sistema</a>
          <a href="#api-jira" class="block text-indigo-600 hover:text-indigo-800">2. Integración con Jira API</a>
          <a href="#configuracion" class="block text-indigo-600 hover:text-indigo-800">3. Configuración Detallada</a>
          <a href="#procesamiento" class="block text-indigo-600 hover:text-indigo-800">4. Procesamiento de Datos</a>
          <a href="#almacenamiento" class="block text-indigo-600 hover:text-indigo-800">5. Almacenamiento y Persistencia</a>
          <a href="#errores" class="block text-indigo-600 hover:text-indigo-800">6. Manejo de Errores</a>
          <a href="#ejemplos" class="block text-indigo-600 hover:text-indigo-800">7. Ejemplos de Uso</a>
        </nav>
      </div>

      <!-- Arquitectura -->
      <div id="arquitectura" class="bg-white rounded-lg shadow p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">1. Arquitectura del Sistema</h2>
        
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-3">Backend (FastAPI)</h3>
          <ul class="space-y-2 text-gray-600">
            <li class="flex items-start">
              <span class="text-indigo-600 mr-2">•</span>
              <span><strong>Endpoint principal:</strong> <code class="bg-gray-100 px-2 py-1 rounded text-sm">/sync-jira-issues</code> - Inicia la sincronización</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-600 mr-2">•</span>
              <span><strong>Status endpoint:</strong> <code class="bg-gray-100 px-2 py-1 rounded text-sm">/sync-status/{task_id}</code> - Consulta el progreso</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-600 mr-2">•</span>
              <span><strong>Tasks endpoint:</strong> <code class="bg-gray-100 px-2 py-1 rounded text-sm">/sync-tasks</code> - Lista todas las tareas</span>
            </li>
          </ul>
        </div>

        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-3">Frontend (Vue 3 + TypeScript)</h3>
          <ul class="space-y-2 text-gray-600">
            <li class="flex items-start">
              <span class="text-indigo-600 mr-2">•</span>
              <span><strong>Store (Pinia):</strong> Gestión centralizada del estado de sincronización</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-600 mr-2">•</span>
              <span><strong>Polling automático:</strong> Actualización cada 2 segundos durante la sincronización</span>
            </li>
            <li class="flex items-start">
              <span class="text-indigo-600 mr-2">•</span>
              <span><strong>LocalStorage:</strong> Persistencia opcional de configuraciones</span>
            </li>
          </ul>
        </div>

        <div class="bg-gray-50 rounded-lg p-4 mt-4">
          <h4 class="font-semibold text-gray-800 mb-2">Flujo de Datos</h4>
          <pre class="text-sm text-gray-600 overflow-x-auto">
Cliente → POST /sync-jira-issues → Task ID
   ↓
Polling → GET /sync-status/{task_id}
   ↓
Backend → Jira API → MySQL
   ↓
Respuesta → Cliente (progreso/resultado)
          </pre>
        </div>
      </div>

      <!-- API Jira -->
      <div id="api-jira" class="bg-white rounded-lg shadow p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">2. Integración con Jira API</h2>
        
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-3">Autenticación</h3>
          <div class="bg-gray-50 rounded-lg p-4">
            <p class="text-gray-600 mb-2">La aplicación utiliza autenticación básica con API Token:</p>
            <code class="block bg-gray-800 text-gray-100 p-3 rounded text-sm">
              Authorization: Basic base64(email:api_token)
            </code>
          </div>
        </div>

        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-3">Endpoints Utilizados</h3>
          <ul class="space-y-3">
            <li>
              <h4 class="font-medium text-gray-700">Conteo de Issues</h4>
              <code class="block bg-gray-100 p-2 rounded text-sm mt-1">
                GET /rest/api/3/search?jql={jql}&maxResults=0
              </code>
            </li>
            <li>
              <h4 class="font-medium text-gray-700">Búsqueda con Paginación</h4>
              <code class="block bg-gray-100 p-2 rounded text-sm mt-1">
                GET /rest/api/3/search?jql={jql}&maxResults={limit}&startAt={offset}
              </code>
            </li>
          </ul>
        </div>

        <div class="bg-blue-50 border-l-4 border-blue-400 p-4">
          <p class="text-blue-700">
            <strong>Nota:</strong> El sistema maneja automáticamente la paginación usando <code>nextPageToken</code> para conjuntos de datos grandes.
          </p>
        </div>
      </div>

      <!-- Configuración -->
      <div id="configuracion" class="bg-white rounded-lg shadow p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">3. Configuración Detallada</h2>
        
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-3">Ejemplo de Configuración JSON</h3>
          <pre class="bg-gray-800 text-gray-100 p-4 rounded-lg text-sm overflow-x-auto">
{
  "jira_domain": "tu-empresa.atlassian.net",
  "jira_email": "tu-email@empresa.com",
  "jira_api_token": "tu-token-api",
  "jql": "project = PROYECTO AND updated >= -7d",
  "fields": {
    "summary": "resumen",
    "status": "estado",
    "customfield_10860": "campo_personalizado",
    "description": "descripcion"
  },
  "mysql_host": "localhost",
  "mysql_port": 3306,
  "mysql_user": "root",
  "mysql_password": "password",
  "mysql_database": "jiradb",
  "mysql_table": "jira_issues",
  "max_results_per_page": 50
}
          </pre>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-3">Campos de Jira</h3>
            <ul class="space-y-2 text-gray-600">
              <li><code class="bg-gray-100 px-2 py-1 rounded text-sm">summary</code> - Título del issue</li>
              <li><code class="bg-gray-100 px-2 py-1 rounded text-sm">status</code> - Estado actual</li>
              <li><code class="bg-gray-100 px-2 py-1 rounded text-sm">description</code> - Descripción completa</li>
              <li><code class="bg-gray-100 px-2 py-1 rounded text-sm">customfield_*</code> - Campos personalizados</li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-3">Tipos de Datos MySQL</h3>
            <ul class="space-y-2 text-gray-600">
              <li><code class="bg-gray-100 px-2 py-1 rounded text-sm">BOOLEAN</code> - Valores true/false</li>
              <li><code class="bg-gray-100 px-2 py-1 rounded text-sm">BIGINT</code> - Números enteros</li>
              <li><code class="bg-gray-100 px-2 py-1 rounded text-sm">DOUBLE</code> - Números decimales</li>
              <li><code class="bg-gray-100 px-2 py-1 rounded text-sm">JSON</code> - Objetos y arrays</li>
              <li><code class="bg-gray-100 px-2 py-1 rounded text-sm">TEXT</code> - Strings y otros</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Procesamiento -->
      <div id="procesamiento" class="bg-white rounded-lg shadow p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">4. Procesamiento de Datos</h2>
        
        <div class="space-y-4">
          <div class="border-l-4 border-indigo-500 pl-4">
            <h3 class="font-semibold text-gray-800 mb-2">1. Conteo Total</h3>
            <p class="text-gray-600">Primero se obtiene el total de issues que coinciden con el JQL para calcular el progreso.</p>
          </div>
          
          <div class="border-l-4 border-indigo-500 pl-4">
            <h3 class="font-semibold text-gray-800 mb-2">2. Descarga por Lotes</h3>
            <p class="text-gray-600">Los issues se descargan en lotes de 50 (configurable) usando paginación.</p>
          </div>
          
          <div class="border-l-4 border-indigo-500 pl-4">
            <h3 class="font-semibold text-gray-800 mb-2">3. Preparación de Tabla</h3>
            <p class="text-gray-600">Se crea la tabla si no existe y se agregan columnas dinámicamente según los campos encontrados.</p>
          </div>
          
          <div class="border-l-4 border-indigo-500 pl-4">
            <h3 class="font-semibold text-gray-800 mb-2">4. Sincronización</h3>
            <p class="text-gray-600">Se usa <code>INSERT ... ON DUPLICATE KEY UPDATE</code> para insertar o actualizar registros.</p>
          </div>
        </div>
      </div>

      <!-- Almacenamiento -->
      <div id="almacenamiento" class="bg-white rounded-lg shadow p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">5. Almacenamiento y Persistencia</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-3">LocalStorage (Frontend)</h3>
            <ul class="space-y-2 text-gray-600">
              <li class="flex items-start">
                <span class="text-green-600 mr-2">✓</span>
                <span>Configuraciones de usuario</span>
              </li>
              <li class="flex items-start">
                <span class="text-green-600 mr-2">✓</span>
                <span>Preferencia de auto-guardado</span>
              </li>
              <li class="flex items-start">
                <span class="text-green-600 mr-2">✓</span>
                <span>Campos mapeados personalizados</span>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-3">MySQL (Backend)</h3>
            <ul class="space-y-2 text-gray-600">
              <li class="flex items-start">
                <span class="text-green-600 mr-2">✓</span>
                <span>Issues de Jira sincronizados</span>
              </li>
              <li class="flex items-start">
                <span class="text-green-600 mr-2">✓</span>
                <span>Tipos de datos automáticos</span>
              </li>
              <li class="flex items-start">
                <span class="text-green-600 mr-2">✓</span>
                <span>Índice único en <code>key</code></span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Manejo de Errores -->
      <div id="errores" class="bg-white rounded-lg shadow p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">6. Manejo de Errores</h2>
        
        <div class="space-y-4">
          <div class="bg-red-50 border-l-4 border-red-400 p-4">
            <h3 class="font-semibold text-red-800 mb-2">Errores de Autenticación</h3>
            <p class="text-red-700">Se validan credenciales y se muestran mensajes claros si el token es inválido.</p>
          </div>
          
          <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4">
            <h3 class="font-semibold text-yellow-800 mb-2">Errores de Conexión</h3>
            <p class="text-yellow-700">Reintentos automáticos y mensajes de estado durante problemas de red.</p>
          </div>
          
          <div class="bg-blue-50 border-l-4 border-blue-400 p-4">
            <h3 class="font-semibold text-blue-800 mb-2">Errores de Base de Datos</h3>
            <p class="text-blue-700">Validación de conexión antes de iniciar y manejo de errores SQL.</p>
          </div>
        </div>
      </div>

      <!-- Ejemplos -->
      <div id="ejemplos" class="bg-white rounded-lg shadow p-8 mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">7. Ejemplos de Uso</h2>
        
        <div class="space-y-6">
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-3">Sincronizar Issues del Último Mes</h3>
            <pre class="bg-gray-100 p-3 rounded text-sm">
JQL: project = TU_PROYECTO AND created >= -30d
            </pre>
          </div>
          
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-3">Sincronizar Solo Bugs Abiertos</h3>
            <pre class="bg-gray-100 p-3 rounded text-sm">
JQL: project = TU_PROYECTO AND issuetype = Bug AND status != Closed
            </pre>
          </div>
          
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-3">Campos Personalizados de Ejemplo</h3>
            <pre class="bg-gray-100 p-3 rounded text-sm">
{
  "summary": "titulo",
  "status": "estado_actual",
  "customfield_10001": "cliente",
  "customfield_10002": "prioridad_negocio"
}
            </pre>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="bg-gray-100 rounded-lg p-6 text-center">
        <p class="text-gray-600">
          ¿Necesitas ayuda? Contacta al equipo de desarrollo o revisa el código fuente.
        </p>
        <div class="mt-4 flex justify-center gap-4">
          <a href="https://github.com" class="text-indigo-600 hover:text-indigo-800 font-medium">
            GitHub
          </a>
          <span class="text-gray-400">•</span>
          <a href="mailto:soporte@empresa.com" class="text-indigo-600 hover:text-indigo-800 font-medium">
            Soporte
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Smooth scroll behavior */
html {
  scroll-behavior: smooth;
}

/* Code blocks styling */
code {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}
</style>
