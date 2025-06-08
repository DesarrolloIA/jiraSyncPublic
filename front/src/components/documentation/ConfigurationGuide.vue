<template>
  <div class="space-y-8">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Guía de Configuración</h2>
    
    <!-- Environment Setup -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Configuración del Entorno</h3>
      
      <div class="space-y-6">
        <!-- Backend .env -->
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Backend (.env)</h4>
          <p class="text-gray-600 mb-3">Crear archivo <code class="bg-gray-100 px-1 rounded">my-fastapi-app/.env</code></p>
          
          <div class="bg-gray-50 rounded p-3">
            <pre class="text-sm"><code># MySQL Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=jiradb

# API Configuration
API_PORT=8000
CORS_ORIGINS=["http://localhost:5173"]

# Optional: Jira Default Values
JIRA_DEFAULT_DOMAIN=your-domain.atlassian.net
JIRA_DEFAULT_EMAIL=your-email@example.com</code></pre>
          </div>
        </div>

        <!-- Frontend .env -->
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Frontend (.env)</h4>
          <p class="text-gray-600 mb-3">Crear archivo <code class="bg-gray-100 px-1 rounded">front/.env</code></p>
          
          <div class="bg-gray-50 rounded p-3">
            <pre class="text-sm"><code># API URL
VITE_API_URL=http://localhost:8000

# Optional: Default Values
VITE_DEFAULT_MYSQL_HOST=localhost
VITE_DEFAULT_MYSQL_PORT=3306
VITE_DEFAULT_MYSQL_DATABASE=jiradb</code></pre>
          </div>
        </div>
      </div>
    </div>

    <!-- Jira Configuration -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Configuración de Jira</h3>
      
      <div class="space-y-4">
        <div class="border-l-4 border-blue-500 pl-4">
          <h4 class="font-semibold mb-2">1. Obtener API Token</h4>
          <ol class="text-sm text-gray-600 space-y-1 list-decimal list-inside">
            <li>Ir a <a href="https://id.atlassian.com/manage-profile/security/api-tokens" class="text-indigo-600 hover:underline" target="_blank">Atlassian API Tokens</a></li>
            <li>Click en "Create API token"</li>
            <li>Dar un nombre descriptivo (ej: "Jira Sync")</li>
            <li>Copiar el token generado</li>
          </ol>
        </div>
        
        <div class="border-l-4 border-blue-500 pl-4">
          <h4 class="font-semibold mb-2">2. Permisos Necesarios</h4>
          <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
            <li>Lectura de proyectos</li>
            <li>Lectura de issues</li>
            <li>Acceso a campos personalizados</li>
          </ul>
        </div>
        
        <div class="border-l-4 border-blue-500 pl-4">
          <h4 class="font-semibold mb-2">3. JQL Query</h4>
          <p class="text-sm text-gray-600 mb-2">Ejemplos de queries JQL:</p>
          <ul class="text-sm font-mono space-y-1">
            <li class="bg-gray-100 p-1 rounded">project = TEST</li>
            <li class="bg-gray-100 p-1 rounded">project = TEST AND updated >= -7d</li>
            <li class="bg-gray-100 p-1 rounded">project in (TEST, PROD) AND status = Open</li>
            <li class="bg-gray-100 p-1 rounded">assignee = currentUser() AND status != Closed</li>
          </ul>
        </div>

        <div class="border-l-4 border-blue-500 pl-4">
          <h4 class="font-semibold mb-2">4. Campos Personalizados</h4>
          <p class="text-sm text-gray-600 mb-2">Para encontrar IDs de campos personalizados:</p>
          <ol class="text-sm text-gray-600 space-y-1 list-decimal list-inside">
            <li>Ir a Configuración → Issues → Campos personalizados</li>
            <li>Click en el campo deseado</li>
            <li>En la URL verás <code class="bg-gray-100 px-1 rounded">customfield_10XXX</code></li>
          </ol>
        </div>
      </div>
    </div>

    <!-- MySQL Configuration -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Configuración de MySQL</h3>
      
      <div class="space-y-4">
        <div class="bg-gray-50 rounded p-4">
          <p class="text-sm font-semibold mb-2">Crear base de datos:</p>
          <pre class="text-sm"><code>CREATE DATABASE IF NOT EXISTS jiradb
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;</code></pre>
        </div>
        
        <div class="bg-gray-50 rounded p-4">
          <p class="text-sm font-semibold mb-2">Crear usuario específico (recomendado):</p>
          <pre class="text-sm"><code>CREATE USER 'jira_sync'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON jiradb.* TO 'jira_sync'@'localhost';
FLUSH PRIVILEGES;</code></pre>
        </div>
        
        <div class="bg-gray-50 rounded p-4">
          <p class="text-sm font-semibold mb-2">Estructura de tablas creadas automáticamente:</p>
          <pre class="text-sm"><code>-- Tabla de issues
CREATE TABLE jira_issues (
  `key` VARCHAR(255) PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  -- Campos dinámicos según configuración
);

-- Tabla de logs
CREATE TABLE sync_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  task_id VARCHAR(255) UNIQUE NOT NULL,
  started_at TIMESTAMP NOT NULL,
  completed_at TIMESTAMP NULL,
  status VARCHAR(50) NOT NULL,
  jql_query TEXT NOT NULL,
  total_issues INT DEFAULT 0,
  processed_issues INT DEFAULT 0,
  error_message TEXT NULL,
  result JSON NULL,
  backup_file VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);</code></pre>
        </div>
      </div>
    </div>

    <!-- Field Mapping -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Mapeo de Campos</h3>
      
      <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
        <p class="text-sm text-blue-700">
          <strong>Tip:</strong> Los campos personalizados de Jira tienen IDs como <code>customfield_10001</code>. 
          Puedes mapearlos a nombres más legibles en MySQL.
        </p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Formato Simple (Lista)</h4>
          <div class="bg-gray-50 rounded p-3">
            <pre class="text-sm"><code>[
  "summary",
  "status",
  "assignee",
  "priority",
  "description"
]</code></pre>
          </div>
          <p class="text-xs text-gray-600 mt-2">Los nombres de columna serán idénticos a los campos de Jira</p>
        </div>
        
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Formato Avanzado (Mapeo)</h4>
          <div class="bg-gray-50 rounded p-3">
            <pre class="text-sm"><code>{
  "summary": "resumen",
  "status": "estado",
  "customfield_10860": "MSISDN",
  "description": "descripcion",
  "assignee": "asignado_a",
  "priority": "prioridad"
}</code></pre>
          </div>
          <p class="text-xs text-gray-600 mt-2">Permite nombres personalizados en MySQL</p>
        </div>
      </div>
    </div>

    <!-- Example Configurations -->
    <div class="mb-8">
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Configuraciones de Ejemplo</h3>
      
      <div class="space-y-4">
        <!-- Configuration 1 -->
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Ejemplo 1: Sincronización Simple</h4>
          <div class="bg-gray-50 rounded p-3">
            <pre class="text-sm"><code>{
  "jira_domain": "mycompany.atlassian.net",
  "jira_email": "user@mycompany.com",
  "jira_api_token": "ATATT3xFfGF0...",
  "jql": "project = DEV",
  "fields": ["summary", "status", "assignee"],
  "mysql_host": "localhost",
  "mysql_port": 3306,
  "mysql_user": "root",
  "mysql_password": "password",
  "mysql_database": "jiradb",
  "mysql_table": "development_issues"
}</code></pre>
          </div>
        </div>

        <!-- Configuration 2 -->
        <div class="border rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 mb-2">Ejemplo 2: Configuración Avanzada</h4>
          <div class="bg-gray-50 rounded p-3">
            <pre class="text-sm"><code>{
  "jira_domain": "enterprise.atlassian.net",
  "jira_email": "admin@enterprise.com",
  "jira_api_token": "ATATT3xFfGF0...",
  "jql": "project = PROD AND updated >= -30d AND type = Bug",
  "fields": {
    "key": "ticket_id",
    "summary": "titulo",
    "status": "estado_actual",
    "customfield_10020": "cliente",
    "customfield_10021": "severidad",
    "description": "descripcion_completa",
    "assignee": "responsable",
    "reporter": "reportado_por",
    "created": "fecha_creacion",
    "updated": "ultima_actualizacion"
  },
  "mysql_host": "prod-db.enterprise.com",
  "mysql_port": 3306,
  "mysql_user": "jira_sync_user",
  "mysql_password": "SecurePass123!",
  "mysql_database": "production_metrics",
  "mysql_table": "bug_tracking"
}</code></pre>
          </div>
        </div>
      </div>
    </div>

    <!-- Troubleshooting -->
    <div>
      <h3 class="text-xl font-semibold text-gray-900 mb-4">Solución de Problemas</h3>
      
      <div class="space-y-4">
        <div class="border-l-4 border-red-500 pl-4">
          <h4 class="font-semibold mb-2">Error: Authentication failed</h4>
          <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
            <li>Verificar que el email sea correcto</li>
            <li>Regenerar el API token en Atlassian</li>
            <li>Confirmar que el dominio incluya <code>.atlassian.net</code></li>
          </ul>
        </div>
        
        <div class="border-l-4 border-red-500 pl-4">
          <h4 class="font-semibold mb-2">Error: MySQL connection refused</h4>
          <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
            <li>Verificar que MySQL esté ejecutándose</li>
            <li>Confirmar puerto (default: 3306)</li>
            <li>Revisar credenciales de usuario</li>
            <li>Verificar permisos de red si es remoto</li>
          </ul>
        </div>
        
        <div class="border-l-4 border-red-500 pl-4">
          <h4 class="font-semibold mb-2">Error: Field not found</h4>
          <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
            <li>Verificar el ID exacto del campo personalizado</li>
            <li>Confirmar permisos de lectura en el campo</li>
            <li>Usar la API de Jira para listar campos disponibles</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Component logic for Configuration Guide
</script>

<style scoped>
code {
  @apply font-mono text-sm;
}

pre code {
  @apply block;
}
</style> 