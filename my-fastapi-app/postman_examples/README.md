# Ejemplos de Postman para API de Logs

## 1. Test de Conexión

**Endpoint:** `POST http://localhost:8000/api/logs/test-connection`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{}
```

**Respuesta esperada:**
```json
{
  "status": "Connected",
  "table_exists": true,
  "row_count": 5,
  "table_structure": [
    {
      "Field": "task_id",
      "Type": "varchar(255)",
      "Null": "NO",
      "Key": "PRI",
      "Default": null,
      "Extra": ""
    },
    // ... más columnas
  ],
  "sample_data": [
    // ... datos de muestra
  ]
}
```

## 2. Obtener Logs por Task ID

**Endpoint:** `POST http://localhost:8000/api/logs/by-task`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "task_id": "168bf3ec-e688-425e-a6c6-b07f548fed3f"
}
```

**Respuesta esperada:**
```json
{
  "task_id": "168bf3ec-e688-425e-a6c6-b07f548fed3f",
  "total_logs": 1,
  "logs": [
    {
      "task_id": "168bf3ec-e688-425e-a6c6-b07f548fed3f",
      "status": "completado",
      "total_issues": 860,
      "processed_issues": 860,
      "created_at": "2025-06-08T03:04:23",
      "backup_file": "jira_sync_2025-06-08_03-04-23.sql",
      // ... más campos
    }
  ],
  "available_columns": [
    "task_id",
    "status",
    "total_issues",
    "processed_issues",
    "created_at",
    "backup_file",
    "error_message"
  ]
}
```

## 3. Cómo usar en Postman

1. Abre Postman
2. Crea una nueva petición
3. Selecciona el método **POST**
4. Ingresa la URL del endpoint
5. En la pestaña **Headers**, agrega:
   - Key: `Content-Type`
   - Value: `application/json`
6. En la pestaña **Body**:
   - Selecciona **raw**
   - Selecciona **JSON** del dropdown
   - Pega el JSON de ejemplo
7. Click en **Send**

## 4. Notas importantes

- El servidor FastAPI debe estar corriendo en `http://localhost:8000`
- La base de datos MySQL debe estar configurada correctamente
- Para obtener un `task_id` válido, primero ejecuta una sincronización y copia el ID devuelto 