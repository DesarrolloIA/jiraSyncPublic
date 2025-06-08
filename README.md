# Jira Sync Manager

Una aplicación full-stack moderna para sincronizar issues de Jira Cloud con una base de datos MySQL, con seguimiento de progreso en tiempo real, auto-guardado de configuraciones y documentación integrada.

## 🚀 Características

- **Sincronización en segundo plano**: Las tareas se ejecutan de forma asíncrona
- **Progreso en tiempo real**: Visualiza el estado y porcentaje de avance
- **Mapeo de campos flexible**: Mapea campos de Jira a nombres personalizados en MySQL
- **Interfaz moderna**: UI construida con Vue 3, Pinia y Tailwind CSS
- **Consola de progreso**: Terminal-like interface para visualizar el estado
- **Historial de tareas**: Visualiza las sincronizaciones anteriores
- **Auto-guardado**: Configuraciones persistentes en localStorage
- **Import/Export JSON**: Comparte configuraciones fácilmente
- **Documentación integrada**: Guías y ejemplos en la aplicación
- **Docker Ready**: Despliega con un solo comando

## 📋 Requisitos

- Python 3.10+
- Node.js 16+
- MySQL 5.7+
- Cuenta de Jira Cloud con API token

## 🛠️ Instalación

### Backend (FastAPI)

```bash
cd my-fastapi-app
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Frontend (Vue 3)

```bash
cd front
npm install
```

## 🐳 Ejecutar con Docker (Recomendado)

La forma más fácil de ejecutar la aplicación es usando Docker Compose:

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd 2-jiraSync

# Construir y ejecutar los contenedores
docker-compose up -d

# Ver los logs
docker-compose logs -f

# Detener la aplicación
docker-compose down
```

La aplicación estará disponible en:
- Frontend: http://localhost
- Backend API: http://localhost:8000

## 🏃‍♂️ Ejecutar manualmente

### 1. Iniciar el backend:

```bash
cd my-fastapi-app
.\venv\Scripts\activate
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Iniciar el frontend:

```bash
cd front
npm run dev
```

### 3. Abrir la aplicación:

Navega a `http://localhost:5173` en tu navegador.

## 📝 Configuración

### Obtener API Token de Jira:

1. Ve a https://id.atlassian.com/manage-profile/security/api-tokens
2. Click en "Create API token"
3. Dale un nombre y copia el token

### Configurar MySQL:

1. Crea una base de datos (ej: `jiradb`)
2. El usuario debe tener permisos CREATE, INSERT, UPDATE, ALTER

## 🎯 Uso

1. **Navega a Jira Sync** en el menú
2. **Completa el formulario**:
   - Credenciales de Jira
   - JQL query (ej: `project = SAC AND updated >= -7d`)
   - Mapeo de campos
   - Configuración de MySQL
3. **Click en "Iniciar Sincronización"**
4. **Observa el progreso** en la consola en tiempo real

## 📊 Ejemplo de Mapeo de Campos

```json
{
  "summary": "resumen",
  "status": "estado",
  "priority": "prioridad",
  "assignee": "asignado_a",
  "customfield_10860": "tipo_cliente"
}
```

## 🔧 API Endpoints

- `POST /sync-jira-issues` - Inicia sincronización en segundo plano
- `GET /sync-status/{task_id}` - Obtiene el estado de una tarea
- `GET /sync-tasks` - Lista las tareas recientes
- `POST /test-jira-connection` - Prueba la conexión con Jira

## 🏗️ Arquitectura

### Backend:
- **FastAPI**: Framework web moderno y rápido
- **MySQL Connector**: Integración con base de datos
- **Threading**: Ejecución de tareas en segundo plano
- **Pydantic**: Validación de datos

### Frontend:
- **Vue 3**: Framework reactivo con Composition API
- **Pinia**: Manejo de estado global
- **Tailwind CSS**: Estilos utilitarios modernos
- **Axios**: Cliente HTTP para API calls
- **TypeScript**: Type safety

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. 