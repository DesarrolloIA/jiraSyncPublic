<template>
  <div class="space-y-8">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Historial de Versiones y Commits</h2>
      
      <!-- Version 2.1 -->
      <div class="mb-8 border-l-4 border-purple-500 pl-6">
        <div class="flex items-center mb-2">
          <h3 class="text-xl font-semibold text-gray-900">Version 2.1</h3>
          <span class="ml-3 px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">Actual</span>
        </div>
        <p class="text-sm text-gray-500 mb-2">Fecha: 9 de Junio, 2025</p>
        <p class="text-sm text-gray-500 mb-4">Commit: <code class="bg-gray-100 px-1 rounded">feat: v2.1 - Docker compose completo con MySQL, phpMyAdmin, scripts de reset y configuración con .env</code></p>
        
        <div class="space-y-6">
          <!-- Docker Compose Mejorado -->
          <div class="bg-purple-50 rounded-lg p-4">
            <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
              🐳 Docker Compose Completo
              <span class="ml-2 px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded">Nuevo</span>
            </h4>
            <p class="text-sm text-gray-700 mb-3">Stack completo con MySQL, phpMyAdmin y healthchecks configurados.</p>
            
            <div class="space-y-2">
              <p class="text-sm font-semibold text-gray-700">Servicios incluidos:</p>
              <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
                <li><strong>Frontend</strong>: Vue 3 + Nginx en puerto 80</li>
                <li><strong>Backend</strong>: FastAPI en puerto 8000</li>
                <li><strong>MySQL 8.0</strong>: Base de datos en puerto 3306</li>
                <li><strong>phpMyAdmin</strong>: Administración DB en puerto 8080</li>
              </ul>
            </div>
            
            <div class="mt-3 bg-white rounded p-3">
              <p class="text-xs font-mono text-gray-600">// Estructura de directorios:</p>
              <pre class="text-xs font-mono">volumes/
├── mysql/     # Datos persistentes de MySQL
└── backups/   # Respaldos de sincronizaciones
config/
├── mysql/     # my.cnf con configuración optimizada
└── phpmyadmin/# Configuración personalizada</pre>
            </div>
          </div>

          <!-- Variables de Entorno -->
          <div class="bg-blue-50 rounded-lg p-4">
            <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
              🔐 Configuración con Variables de Entorno
              <span class="ml-2 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">Nuevo</span>
            </h4>
            <p class="text-sm text-gray-700 mb-3">Sistema centralizado de configuración usando archivo .env.</p>
            
            <div class="space-y-2">
              <p class="text-sm font-semibold text-gray-700">Variables disponibles:</p>
              <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
                <li><code class="bg-gray-100 px-1 rounded text-xs">MYSQL_ROOT_PASSWORD</code>: Contraseña de MySQL</li>
                <li><code class="bg-gray-100 px-1 rounded text-xs">MYSQL_DATABASE</code>: Base de datos (jiradb)</li>
                <li><code class="bg-gray-100 px-1 rounded text-xs">FRONTEND_PORT</code>: Puerto del frontend (80)</li>
                <li><code class="bg-gray-100 px-1 rounded text-xs">BACKEND_PORT</code>: Puerto del backend (8000)</li>
                <li><code class="bg-gray-100 px-1 rounded text-xs">PHPMYADMIN_PORT</code>: Puerto de phpMyAdmin (8080)</li>
              </ul>
            </div>
            
            <div class="mt-3 bg-white rounded p-3">
              <p class="text-xs font-mono text-gray-600">// Uso:</p>
              <p class="text-xs font-mono">1. cp env.example .env</p>
              <p class="text-xs font-mono">2. Editar .env con tus valores</p>
              <p class="text-xs font-mono">3. docker compose up -d</p>
            </div>
          </div>

          <!-- Scripts de Reset -->
          <div class="bg-green-50 rounded-lg p-4">
            <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
              🔄 Scripts de Reset Multi-plataforma
              <span class="ml-2 px-2 py-1 bg-green-100 text-green-800 text-xs rounded">Nuevo</span>
            </h4>
            <p class="text-sm text-gray-700 mb-3">Scripts interactivos para reiniciar y limpiar la aplicación en Windows y Linux.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="text-sm font-semibold text-gray-700 mb-2">Linux/Unix (reset.sh):</p>
                <pre class="text-xs font-mono bg-gray-100 p-2 rounded">./reset.sh</pre>
              </div>
              <div>
                <p class="text-sm font-semibold text-gray-700 mb-2">Windows (reset.ps1):</p>
                <pre class="text-xs font-mono bg-gray-100 p-2 rounded">.\reset.ps1</pre>
              </div>
            </div>
            
            <div class="mt-3">
              <p class="text-sm font-semibold text-gray-700 mb-2">Opciones del menú:</p>
              <ol class="text-sm text-gray-600 space-y-1 list-decimal list-inside">
                <li>Reiniciar todo (datos + configuraciones)</li>
                <li>Reiniciar solo datos de MySQL</li>
                <li>Reiniciar solo backups</li>
                <li>Reiniciar configuraciones</li>
              </ol>
            </div>
          </div>

          <!-- Correcciones Técnicas -->
          <div class="bg-orange-50 rounded-lg p-4">
            <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
              🔧 Correcciones y Mejoras Técnicas
              <span class="ml-2 px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded">Corregido</span>
            </h4>
            <p class="text-sm text-gray-700 mb-3">Solución de problemas de conectividad y compatibilidad.</p>
            
            <ul class="text-sm text-gray-600 space-y-2 list-disc list-inside">
              <li><strong>CORS actualizado</strong>: Ahora acepta peticiones desde puertos 80, 5173, 3000</li>
              <li><strong>MySQL 8.0 estable</strong>: Cambiado de 'latest' a '8.0' para evitar incompatibilidades</li>
              <li><strong>SyncLogsViewer</strong>: Usa variable VITE_API_URL en lugar de localhost hardcodeado</li>
              <li><strong>Healthchecks</strong>: Configurados para todos los servicios con reintentos</li>
              <li><strong>Dependencias</strong>: Backend y phpMyAdmin esperan que MySQL esté healthy</li>
              <li><strong>TypeScript</strong>: Actualizado tsconfig para ES2020 y mejor compatibilidad</li>
            </ul>
            
            <div class="mt-3 bg-white rounded p-3">
              <p class="text-xs font-mono text-gray-600">// Archivos modificados:</p>
              <p class="text-xs font-mono">- docker-compose.yml</p>
              <p class="text-xs font-mono">- my-fastapi-app/main.py (CORS)</p>
              <p class="text-xs font-mono">- front/src/components/SyncLogsViewer.vue</p>
              <p class="text-xs font-mono">- config/mysql/my.cnf</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Version 2.0 -->
      <div class="mb-8 border-l-4 border-indigo-500 pl-6">
        <div class="flex items-center mb-2">
          <h3 class="text-xl font-semibold text-gray-900">Version 2.0</h3>
          <span class="ml-3 px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">Anterior</span>
        </div>
        <p class="text-sm text-gray-500 mb-2">Fecha: 8 de Junio, 2025</p>
        <p class="text-sm text-gray-500 mb-4">Commit: <code class="bg-gray-100 px-1 rounded">feat: v2.0 - Sistema completo Jira-MySQL con logs, backups, import/export JSON y UI moderna</code></p>
        
        <div class="space-y-6">
          <!-- Sistema de Logs -->
          <div class="bg-blue-50 rounded-lg p-4">
            <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
              📊 Sistema de Logs Completo
              <span class="ml-2 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">Nuevo</span>
            </h4>
            <p class="text-sm text-gray-700 mb-3">Vista dedicada con interfaz tipo terminal para gestionar el historial completo de sincronizaciones.</p>
            
            <div class="space-y-2">
              <p class="text-sm font-semibold text-gray-700">Cómo usar:</p>
              <ol class="text-sm text-gray-600 space-y-1 list-decimal list-inside">
                <li>Desde la vista principal, hacer click en "Ver Logs Completos" en el header</li>
                <li>Se mostrará una consola con todos los logs de sincronización</li>
                <li>Cada log incluye: fecha, duración, issues procesados, estado</li>
                <li>Acciones disponibles: descargar backup, ver detalles, eliminar</li>
              </ol>
            </div>
            
            <div class="mt-3 bg-white rounded p-3">
              <p class="text-xs font-mono text-gray-600">// Endpoints relacionados:</p>
              <p class="text-xs font-mono">GET /api/logs/all</p>
              <p class="text-xs font-mono">DELETE /api/logs/{task_id}</p>
              <p class="text-xs font-mono">POST /api/logs/reset-table</p>
            </div>
          </div>

          <!-- Gestión de Backups -->
          <div class="bg-green-50 rounded-lg p-4">
            <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
              💾 Gestión de Backups SQL
              <span class="ml-2 px-2 py-1 bg-green-100 text-green-800 text-xs rounded">Nuevo</span>
            </h4>
            <p class="text-sm text-gray-700 mb-3">Generación automática de respaldos SQL después de cada sincronización exitosa.</p>
            
            <div class="space-y-2">
              <p class="text-sm font-semibold text-gray-700">Características:</p>
              <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
                <li>Archivo SQL completo con estructura y datos</li>
                <li>Nombrado automático: <code class="bg-gray-100 px-1 rounded text-xs">jira_sync_YYYY-MM-DD_HH-MM-SS.sql</code></li>
                <li>Descarga directa desde la interfaz</li>
                <li>Almacenamiento en <code class="bg-gray-100 px-1 rounded text-xs">./backups/</code></li>
              </ul>
            </div>
            
            <div class="mt-3 bg-white rounded p-3">
              <p class="text-xs font-mono text-gray-600">// Cómo descargar:</p>
              <p class="text-xs font-mono">1. Ir a "Ver Logs Completos"</p>
              <p class="text-xs font-mono">2. Click en icono de descarga en cualquier log</p>
              <p class="text-xs font-mono">3. El archivo SQL se descargará automáticamente</p>
            </div>
          </div>

          <!-- Import/Export JSON -->
          <div class="bg-purple-50 rounded-lg p-4">
            <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
              📋 Import/Export de Configuración
              <span class="ml-2 px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded">Nuevo</span>
            </h4>
            <p class="text-sm text-gray-700 mb-3">Guarda y carga configuraciones completas en formato JSON.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="text-sm font-semibold text-gray-700 mb-2">Exportar:</p>
                <ol class="text-sm text-gray-600 space-y-1 list-decimal list-inside">
                  <li>Click en "Exportar JSON"</li>
                  <li>Se descarga archivo con fecha</li>
                  <li>Incluye todas las configuraciones</li>
                </ol>
              </div>
              <div>
                <p class="text-sm font-semibold text-gray-700 mb-2">Importar:</p>
                <ol class="text-sm text-gray-600 space-y-1 list-decimal list-inside">
                  <li>Click en "Importar Archivo"</li>
                  <li>Seleccionar archivo JSON</li>
                  <li>O pegar JSON directamente</li>
                </ol>
              </div>
            </div>
            
            <div class="mt-3 bg-white rounded p-3">
              <p class="text-xs font-mono text-gray-600">// Formato del archivo:</p>
              <pre class="text-xs font-mono overflow-x-auto">{
  "jira_domain": "domain.atlassian.net",
  "jira_email": "email@example.com",
  "jira_api_token": "***",
  "jql": "project = TEST",
  "fields": { "summary": "resumen" },
  "mysql_config": { ... }
}</pre>
            </div>
          </div>

          <!-- UI Improvements -->
          <div class="bg-orange-50 rounded-lg p-4">
            <h4 class="font-semibold text-gray-900 mb-3 flex items-center">
              🎨 Mejoras de Interfaz
              <span class="ml-2 px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded">Mejorado</span>
            </h4>
            <p class="text-sm text-gray-700 mb-3">Rediseño completo con componentes modernos y responsive.</p>
            
            <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
              <li>Cards con gradientes y sombras suaves</li>
              <li>Animaciones de hover y transiciones</li>
              <li>Diseño responsive para móviles</li>
              <li>Modales de confirmación para acciones destructivas</li>
              <li>Iconos y feedback visual mejorado</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Version 1.5 -->
      <div class="mb-8 border-l-4 border-yellow-400 pl-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-2">Version 1.5</h3>
        <p class="text-sm text-gray-500 mb-2">Fecha: 7 de Junio, 2025 - 18:00</p>
        <p class="text-sm text-gray-500 mb-4">Commit: <code class="bg-gray-100 px-1 rounded">fix: Responsive design improvements</code></p>
        
        <div class="space-y-4">
          <div>
            <h4 class="font-semibold text-gray-900 mb-2">📱 Diseño Responsive</h4>
            <ul class="list-disc list-inside space-y-1 text-gray-600 text-sm">
              <li>Tamaños de texto adaptativos (xs → sm → lg)</li>
              <li>Grid layouts dinámicos (1 col móvil → 2 cols desktop)</li>
              <li>Ajuste de altura de consola según pantalla</li>
              <li>Botones con textos abreviados en móvil</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Version 1.0 -->
      <div class="mb-8 border-l-4 border-gray-300 pl-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-2">Version 1.0</h3>
        <p class="text-sm text-gray-500 mb-2">Fecha: 7 de Junio, 2025</p>
        <p class="text-sm text-gray-500 mb-4">Commit: <code class="bg-gray-100 px-1 rounded">feat: Initial Jira-MySQL sync implementation</code></p>
        
        <div class="space-y-4">
          <div class="bg-gray-50 rounded-lg p-4">
            <h4 class="font-semibold text-gray-900 mb-2">✨ Características Base</h4>
            <p class="text-sm text-gray-700 mb-3">Implementación inicial del sistema de sincronización.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="text-sm font-semibold text-gray-700 mb-2">Backend:</p>
                <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
                  <li>FastAPI con endpoints async</li>
                  <li>Conexión Jira Cloud API</li>
                  <li>Mapeo dinámico de campos</li>
                  <li>Creación automática de tablas</li>
                </ul>
              </div>
              <div>
                <p class="text-sm font-semibold text-gray-700 mb-2">Frontend:</p>
                <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
                  <li>Vue 3 + TypeScript</li>
                  <li>Formulario de configuración</li>
                  <li>Consola de progreso real-time</li>
                  <li>Historial de tareas recientes</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Future Roadmap -->
      <div class="mt-12 p-6 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg">
        <h3 class="text-xl font-semibold text-gray-900 mb-4">🚀 Roadmap Futuro</h3>
        
        <div class="space-y-3">
          <div class="flex items-start">
            <span class="text-2xl mr-3">📅</span>
            <div>
              <p class="font-semibold text-gray-900">Sincronización Programada</p>
              <p class="text-sm text-gray-600">Cron jobs para sincronización automática</p>
            </div>
          </div>
          
          <div class="flex items-start">
            <span class="text-2xl mr-3">🔄</span>
            <div>
              <p class="font-semibold text-gray-900">Sincronización Bidireccional</p>
              <p class="text-sm text-gray-600">Actualizar Jira desde cambios en MySQL</p>
            </div>
          </div>
          
          <div class="flex items-start">
            <span class="text-2xl mr-3">📊</span>
            <div>
              <p class="font-semibold text-gray-900">Dashboard Analytics</p>
              <p class="text-sm text-gray-600">Métricas y visualizaciones de datos</p>
            </div>
          </div>
          
          <div class="flex items-start">
            <span class="text-2xl mr-3">🔐</span>
            <div>
              <p class="font-semibold text-gray-900">Autenticación de Usuarios</p>
              <p class="text-sm text-gray-600">Sistema de login y permisos</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Component logic for Version History
</script>

<style scoped>
code {
  @apply font-mono text-sm;
}

pre code {
  @apply block;
}
</style> 