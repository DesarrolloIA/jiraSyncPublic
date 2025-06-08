# Nueva Funcionalidad: Visor de Logs de Sincronización

## Descripción
Se ha implementado un visor completo de logs de sincronización con interfaz tipo consola de terminal.

## Características

### 1. Vista de Logs en Consola
- Interfaz tipo terminal con tema oscuro
- Muestra todos los logs de sincronización en formato de consola
- Información detallada de cada sincronización:
  - Task ID
  - Estado (con colores según el estado)
  - Fecha y hora
  - Cantidad de issues procesados
  - Nombre del archivo de backup

### 2. Acciones Disponibles

#### Botón "Ver Logs Completos"
- Ubicado en el header principal
- Alterna entre la vista de sincronización y la vista de logs
- Color púrpura para distinguirlo de otras acciones

#### Botón "Actualizar"
- Recarga los logs desde la base de datos
- Muestra el estado más reciente de todas las sincronizaciones

#### Botón "Reset Tabla"
- Elimina TODOS los registros de la tabla `sync_logs`
- Elimina TODOS los archivos de backup físicos asociados
- Muestra confirmación antes de ejecutar
- Reporta cantidad de archivos eliminados exitosamente

### 3. Acciones por Log Individual

#### Descargar Backup (ícono de descarga)
- Descarga el archivo SQL de backup asociado
- Solo visible si existe archivo de backup

#### Ver Detalles (ícono de ojo)
- Placeholder para futura implementación
- Mostrará detalles completos del log

#### Eliminar (ícono de basura)
- Elimina el registro de la base de datos
- Elimina el archivo de backup físico asociado
- Muestra confirmación antes de ejecutar

## Endpoints API Implementados

### 1. GET `/api/logs/all`
Obtiene todos los logs de sincronización.

**Respuesta:**
```json
{
  "success": true,
  "logs": [
    {
      "task_id": "168bf3ec-e688-425e-a6c6-b07f548fed3f",
      "status": "completado",
      "total_issues": 860,
      "processed_issues": 860,
      "created_at": "2025-06-08T03:04:04",
      "backup_file": "jira_sync_2025-06-08_03-04-23.sql",
      "error_message": null,
      "jql_query": "project = SAC AND updated >= '2025-06-06'"
    }
  ],
  "total": 1
}
```

### 2. DELETE `/api/logs/{task_id}`
Elimina un log específico y su archivo de backup.

**Respuesta:**
```json
{
  "success": true,
  "message": "Log {task_id} eliminado exitosamente",
  "backup_file_deleted": true,
  "backup_file": "jira_sync_2025-06-08_03-04-23.sql"
}
```

### 3. POST `/api/logs/reset-table`
Resetea la tabla completa y elimina todos los backups.

**Respuesta:**
```json
{
  "success": true,
  "message": "Tabla de logs reseteada exitosamente",
  "deleted_files": 5,
  "failed_files": 0,
  "details": {
    "deleted": ["file1.sql", "file2.sql"],
    "failed": []
  }
}
```

## Componentes Vue

### SyncLogsViewer.vue
- Componente principal del visor de logs
- Maneja toda la lógica de visualización y acciones
- Incluye modales de confirmación para acciones destructivas

## Estilos
- Tema oscuro tipo terminal
- Fuente monoespaciada (Consolas, Monaco, Courier New)
- Colores por estado:
  - Verde: completado
  - Amarillo: en progreso
  - Rojo: error
  - Gris: otros estados

## Seguridad
- Confirmaciones antes de acciones destructivas
- Manejo de errores con mensajes descriptivos
- Validación de existencia de archivos antes de eliminar

## Uso

1. Click en "Ver Logs Completos" en el header principal
2. La vista cambiará al visor de logs tipo consola
3. Usa los botones de acción según necesites
4. Click en "Ver Sincronización" para volver a la vista normal

## Notas Importantes

⚠️ **ADVERTENCIA**: El botón "Reset Tabla" eliminará TODOS los registros y archivos de backup de forma permanente. Esta acción NO se puede deshacer.

💡 **TIP**: Los archivos de backup se pueden descargar haciendo click en el ícono de descarga en cada log individual. 