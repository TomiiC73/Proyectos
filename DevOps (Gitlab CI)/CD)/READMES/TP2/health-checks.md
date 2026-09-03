# Verificación de Servicios Deployados

## URLs de Acceso

Todos los servicios están expuestos mediante HTTPS a través del proxy Nginx:

- **Frontend**: https://172.16.9.31:60143/
- **API Root**: https://172.16.9.31:60143/api/
- **API Todos**: https://172.16.9.31:60143/api/todos
- **Notifications (health)**: https://172.16.9.31:60143/notifications/health
- **Notifications (send)** [POST]: https://172.16.9.31:60143/notifications/send
- **Nginx Health**: https://172.16.9.31:60143/health

## Health Checks por Servicio

### 1. Base de Datos (MySQL)

**Health Check interno (Docker)**:
```bash
docker exec todos-db mysqladmin ping -h localhost --silent
```

**Verificación manual**:
```bash
docker exec -it todos-db sh -c "mysql -u todos_user -p$(cat /run/secrets/db_password) -e 'SELECT 1' todos_db"
```

**Estado esperado**: `healthy`

---

### 2. API Backend (Flask)

**Health Check interno (Docker)**:
```bash
docker exec todos-api python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')"
```

**Endpoints disponibles**:

- **GET /** - Bienvenida a la API
  ```bash
  curl -k https://172.16.9.31:60143/api/
  ```
  Respuesta esperada: `{"message":"Bienvenido a la API de Tareas con MySQL"}`

- **GET /todos** - Listar todas las tareas
  ```bash
  curl -k https://172.16.9.31:60143/api/todos
  ```

- **POST /todos** - Crear nueva tarea
  ```bash
  curl -k -X POST https://172.16.9.31:60143/api/todos \
    -H "Content-Type: application/json" \
    -d '{"title":"Nueva tarea"}'
  ```

- **PUT /todos/:id** - Actualizar tarea
  ```bash
  curl -k -X PUT https://172.16.9.31:60143/api/todos/1 \
    -H "Content-Type: application/json" \
    -d '{"title":"Tarea actualizada","completed":true}'
  ```

- **DELETE /todos/:id** - Eliminar tarea
  ```bash
  curl -k -X DELETE https://172.16.9.31:60143/api/todos/1
  ```

**Estado esperado**: `healthy`

---

### 3. Frontend Web (React)

**Health Check interno (Docker)**:
```bash
docker exec todos-web curl -f http://localhost:3000/health
```

**Verificación externa**:
```bash
curl -k https://172.16.9.31:60143/
```

**Estado esperado**: `healthy`

---

### 4. Notifications (FastAPI)

**Health Check interno (Docker)**:
```bash
docker exec todos-notifications curl -f http://localhost:8001/health
```

**Endpoint de health**:
```bash
curl -k https://172.16.9.31:60143/notifications/health
```

Respuesta esperada:
```json
{
  "status":"🟢 Healthy",
  "service":"Notifications Service",
  "timestamp":"2025-11-27T03:36:30.241265"
}
```

**Estado esperado**: `healthy`

**Enviar notificación (POST /notifications/send)**:
```bash
curl -k -X POST https://172.16.9.31:60143/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "type": "email",
    "title": "Prueba de notificación",
    "message": "Hola desde el sistema de notificaciones",
    "recipient": "usuario@example.com",
    "isHtml": false
  }'
```
Notas:
- Con secretos SMTP reales (`smtp_username` y `smtp_password`) envía correo real; si no, simula envío y responde éxito.

---

### 5. Nginx Gateway

**Health Check interno (Docker)**:
```bash
docker exec todos-nginx wget --no-verbose --tries=1 --spider http://localhost/health
```

**Verificación de redirección HTTP → HTTPS**:
```bash
curl -I http://172.16.9.31:60180/
```
Respuesta esperada: `301 Moved Permanently`

**Verificación de HTTPS**:
```bash
curl -k -I https://172.16.9.31:60143/
```
Respuesta esperada: `200 OK`

**Verificación de health de Nginx (en 443)**:
```bash
curl -k https://172.16.9.31:60143/health
```
Respuesta esperada: `healthy`

**Estado esperado**: `healthy`

---

## Verificación Completa del Sistema

### Ver estado de todos los contenedores:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Ver logs de un servicio específico:
```bash
docker logs todos-nginx --tail 50
docker logs todos-api --tail 50
docker logs todos-db --tail 50
docker logs todos-web --tail 50
docker logs todos-notifications --tail 50
```

### Test automatizado (ejecutado por el pipeline):

El pipeline ejecuta automáticamente tests de producción que verifican:

1. Estado de contenedores
2. Puertos expuestos
3. HTTPS funcional
4. HTTP → HTTPS redirect
5. API endpoints respondiendo
6. Frontend accesible
7. Notifications service activo

Los resultados se guardan como artefactos en el job `production-tests:health-checks`.

---

## Troubleshooting

### Si un contenedor está unhealthy:

1. Revisar logs: `docker logs <container-name>`
2. Verificar health check: `docker inspect <container-name> | grep -A 10 Health`
3. Entrar al contenedor: `docker exec -it <container-name> sh`

### Si no hay conectividad:

1. Verificar red: `docker network inspect app-network`
2. Verificar DNS interno: `docker exec todos-api ping todos-db`
3. Verificar puertos: `docker port todos-nginx`
