<template>
  <div class="space-y-8">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Arquitectura del Sistema</h2>
    
    <!-- System Overview -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Vista General</h3>
      
      <div class="bg-gray-50 rounded-lg p-6">
        <pre class="text-sm">
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│                 │     │                  │     │                 │
│   Vue 3 + TS    │────▶│  FastAPI Backend │────▶│   MySQL DB      │
│   (Frontend)    │     │     (Python)     │     │                 │
│                 │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │                         ▲
        │                        │                         │
        │                        ▼                         │
        │               ┌──────────────────┐               │
        │               │                  │               │
        └──────────────▶│   Jira Cloud    │───────────────┘
                        │      API         │
                        │                  │
                        └──────────────────┘
        </pre>
      </div>
    </div>

    <!-- Tech Stack -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Stack Tecnológico</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">Frontend</h4>
          <ul class="space-y-2 text-sm">
            <li class="flex items-center">
              <span class="w-24 text-gray-600">Framework:</span>
              <span class="font-mono">Vue 3 (Composition API)</span>
            </li>
            <li class="flex items-center">
              <span class="w-24 text-gray-600">Lenguaje:</span>
              <span class="font-mono">TypeScript</span>
            </li>
            <li class="flex items-center">
              <span class="w-24 text-gray-600">Estilos:</span>
              <span class="font-mono">Tailwind CSS</span>
            </li>
            <li class="flex items-center">
              <span class="w-24 text-gray-600">Estado:</span>
              <span class="font-mono">Pinia</span>
            </li>
            <li class="flex items-center">
              <span class="w-24 text-gray-600">Router:</span>
              <span class="font-mono">Vue Router</span>
            </li>
            <li class="flex items-center">
              <span class="w-24 text-gray-600">HTTP:</span>
              <span class="font-mono">Axios</span>
            </li>
          </ul>
        </div>
        
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-3">Backend</h4>
          <ul class="space-y-2 text-sm">
            <li class="flex items-center">
              <span class="w-24 text-gray-600">Framework:</span>
              <span class="font-mono">FastAPI</span>
            </li>
            <li class="flex items-center">
              <span class="w-24 text-gray-600">Lenguaje:</span>
              <span class="font-mono">Python 3.9+</span>
            </li>
            <li class="flex items-center">
              <span class="w-24 text-gray-600">DB Driver:</span>
              <span class="font-mono">mysql-connector-python</span>
            </li>
            <li class="flex items-center">
              <span class="w-24 text-gray-600">Validación:</span>
              <span class="font-mono">Pydantic</span>
            </li>
            <li class="flex items-center">
              <span class="w-24 text-gray-600">Async:</span>
              <span class="font-mono">asyncio + threading</span>
            </li>
            <li class="flex items-center">
              <span class="w-24 text-gray-600">CORS:</span>
              <span class="font-mono">fastapi.middleware.cors</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Data Flow -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Flujo de Datos</h3>
      
      <div class="space-y-4">
        <div class="border-l-4 border-indigo-500 pl-4">
          <h4 class="font-semibold mb-2">1. Configuración</h4>
          <p class="text-sm text-gray-600">Usuario configura credenciales Jira y MySQL → Se guarda en localStorage → Se valida la conexión</p>
        </div>
        
        <div class="border-l-4 border-indigo-500 pl-4">
          <h4 class="font-semibold mb-2">2. Sincronización</h4>
          <p class="text-sm text-gray-600">Frontend envía POST → Backend crea tarea async → Polling del estado → Descarga issues de Jira → Mapeo de campos → Insert/Update en MySQL</p>
        </div>
        
        <div class="border-l-4 border-indigo-500 pl-4">
          <h4 class="font-semibold mb-2">3. Respaldo</h4>
          <p class="text-sm text-gray-600">Al completar → Genera SQL dump → Guarda en /backups → Registra en sync_logs → Disponible para descarga</p>
        </div>
        
        <div class="border-l-4 border-indigo-500 pl-4">
          <h4 class="font-semibold mb-2">4. Visualización</h4>
          <p class="text-sm text-gray-600">Frontend consulta logs → Muestra en consola/cards → Acciones disponibles → Actualización reactiva</p>
        </div>
      </div>
    </div>

    <!-- Security Considerations -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Consideraciones de Seguridad</h3>
      
      <div class="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
        <p class="text-sm text-red-700">
          <strong>⚠️ Importante:</strong> Este es un prototipo de desarrollo. Para producción, implementar las siguientes medidas de seguridad.
        </p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Backend Security</h4>
          <ul class="text-sm space-y-1 list-disc list-inside">
            <li>Usar variables de entorno para credenciales</li>
            <li>Implementar autenticación JWT</li>
            <li>Rate limiting en endpoints</li>
            <li>Validación estricta de inputs</li>
            <li>HTTPS obligatorio</li>
          </ul>
        </div>
        
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Frontend Security</h4>
          <ul class="text-sm space-y-1 list-disc list-inside">
            <li>No almacenar tokens en localStorage</li>
            <li>Usar httpOnly cookies</li>
            <li>Sanitizar inputs del usuario</li>
            <li>CSP headers configurados</li>
            <li>XSS protection</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Performance Optimization -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Optimización de Rendimiento</h3>
      
      <div class="space-y-4">
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Sincronización por Lotes</h4>
          <p class="text-sm text-gray-600 mb-2">Para grandes volúmenes de datos:</p>
          <ul class="text-sm space-y-1 list-disc list-inside text-gray-600">
            <li>Procesar issues en lotes de 100-500</li>
            <li>Usar transacciones MySQL para cada lote</li>
            <li>Implementar retry logic para fallos</li>
            <li>Progress tracking detallado por lote</li>
          </ul>
        </div>
        
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Caché y Optimizaciones</h4>
          <ul class="text-sm space-y-1 list-disc list-inside text-gray-600">
            <li>Redis para caché de configuraciones</li>
            <li>Connection pooling para MySQL</li>
            <li>Lazy loading en frontend</li>
            <li>Compresión de respuestas HTTP</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Monitoring & Logging -->
    <div>
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Monitoreo y Logging</h3>
      
      <div class="bg-blue-50 rounded-lg p-4">
        <h4 class="font-semibold text-gray-900 mb-2">Stack de Monitoreo Recomendado</h4>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
          <div class="bg-white rounded p-3">
            <p class="font-semibold text-sm mb-1">Logs</p>
            <p class="text-xs text-gray-600">ELK Stack (Elasticsearch, Logstash, Kibana)</p>
          </div>
          <div class="bg-white rounded p-3">
            <p class="font-semibold text-sm mb-1">Métricas</p>
            <p class="text-xs text-gray-600">Prometheus + Grafana</p>
          </div>
          <div class="bg-white rounded p-3">
            <p class="font-semibold text-sm mb-1">APM</p>
            <p class="text-xs text-gray-600">New Relic o DataDog</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Component logic for Architecture Documentation
</script>

<style scoped>
code {
  @apply font-mono text-sm;
}

pre code {
  @apply block;
}
</style> 