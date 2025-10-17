# Glosario de Errores - Proceso de Dockerización

Este documento registra los principales errores encontrados durante el proceso de dockerización de la aplicación TODO y las soluciones aplicadas.

## Índice de Errores

1. [Error de Conexión a Base de Datos](#-error-de-conexión-a-base-de-datos)
2. [Sistema de Notificaciones Fallido](#-sistema-de-notificaciones-fallido)  
3. [Problemas de Build de Contenedores](#-problemas-de-build-de-contenedores)
4. [Exposición de Secretos en el Repositorio](#-exposición-de-secretos-en-el-repositorio)
5. [Configuración de Nginx y Proxy Reverso](#-configuración-de-nginx-y-proxy-reverso)
6. [Problemas de Dependencias y Puertos](#-problemas-de-dependencias-y-puertos)

---

## Error de Conexión a Base de Datos

### **Error Encontrado**
```bash
Error de conexión a la base de datos MySQL 9.4
mysql.connector.errors.DatabaseError: 2003 (HY000): Can't connect to MySQL server on 'db:3306'
PyMySQL.err.OperationalError: (2003, "Can't connect to MySQL server on 'todos-db:3306'")
```

### **Causa Raíz**
- La aplicación Flask 3.0 intentaba conectarse a MySQL 9.4 antes de la inicialización completa
- Falta de health checks optimizados en docker-compose.yml
- Volúmenes corruptos de Docker que impedían la correcta inicialización de la BD
- Recursos insuficientes asignados al contenedor MySQL

### **Solución Aplicada**
1. **Agregado de depends_on con condition:**
```yaml
api:
  depends_on:
    db:
      condition: service_healthy
```

2. **Health checks optimizados para MySQL 9.4:**
```yaml
db:
  healthcheck:
    test: [ "CMD", "mysqladmin", "ping", "-h", "localhost" ]
    interval: 10s      # Verificación cada 10s
    timeout: 15s       # Timeout de 15s  
    retries: 8         # 8 reintentos máximo
    start_period: 30s  # Período de gracia inicial
```

3. **Asignación automática de recursos:**
```yaml
db:
  deploy:
    resources:
      limits:
        cpus: '2.0'      # 2 CPUs para MySQL 9.4
        memory: 1G       # 1GB RAM garantizada
      reservations:
        cpus: '1.0'      # Mínimo 1 CPU reservada
        memory: 512M     # Mínimo 512MB reservada
```

4. **Reset completo de volúmenes:**
```bash
docker-compose down -v --remove-orphans  # Eliminar volúmenes
docker-compose up -d --build             # Recrear con build
```

### **Lección Aprendida**
Los contenedores de base de datos requieren tiempo de inicialización. Siempre usar health checks y depends_on para garantizar el orden correcto de inicio.

---

## Sistema de Notificaciones Fallido (FastAPI 0.115)

### **Error Encontrado**
```bash
# Errores del servicio de notificaciones FastAPI 0.115
smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted')
uvicorn.error: Error loading ASGI app. Could not import module "simple_app"
ConnectionError: Notification service unavailable on todos-notifications:8001
```

### **Causa Raíz**
- Uso de credenciales hardcodeadas en el código FastAPI
- Intento inicial con servidor SMTP falso (smtp4dev)
- Configuración incorrecta de Gmail SMTP
- Recursos insuficientes asignados al contenedor FastAPI
- Falta de health checks para el servicio de notificaciones

### **Solución Aplicada**
1. **Configuración FastAPI 0.115 con SMTP real:**
```python
# simple_app.py - Servicio FastAPI optimizado
from fastapi import FastAPI
import smtplib
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = read_secret('smtp_username')  # Docker Secret
SMTP_PASSWORD = read_secret('smtp_password')  # Docker Secret
```

2. **Asignación de recursos para FastAPI:**
```yaml
notifications:
  image: todos-notifications:latest
  container_name: todos-notifications
  deploy:
    resources:
      limits:
        cpus: '0.5'      # 0.5 CPU para FastAPI
        memory: 256M     # 256MB RAM
      reservations:
        cpus: '0.2'      # Mínimo 0.2 CPU
        memory: 128M     # Mínimo 128MB
```

3. **Health check para notificaciones:**
```yaml
notifications:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
    interval: 15s
    timeout: 8s
    retries: 4
    start_period: 25s
```

4. **Implementación de Docker Secrets:**
```yaml
secrets:
  smtp_username:
    file: ./secrets/smtp_username.txt
  smtp_password:
    file: ./secrets/smtp_password.txt
```

3. **Función segura para leer secretos:**
```python
def read_secret(secret_name):
    try:
        with open(f'/run/secrets/{secret_name}', 'r') as secret_file:
            return secret_file.read().strip()
    except FileNotFoundError:
        return os.getenv(secret_name.upper())
```

### **Lección Aprendida**
Nunca usar credenciales hardcodeadas. Implementar desde el inicio un sistema de gestión de secretos robusto.

---

## Problemas de Build de Contenedores

### **Error Encontrado**
```bash
ERROR [api 4/6] RUN pip install -r requirements.txt
ModuleNotFoundError: No module named 'flask'
```

### **Causa Raíz**
- Dockerfile mal estructurado con COPY incorrectos
- Dependencias no instaladas en el orden correcto
- Falta de multi-stage builds causando imágenes muy pesadas

### **Solución Aplicada**
1. **Restructuración del Dockerfile con Alpine:**
```dockerfile
# Single-stage build optimizado con Alpine
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .

# Instalar dependencias del sistema y Python packages
RUN apk update \
    && apk add --no-cache --virtual .build-deps \
    gcc musl-dev mariadb-dev python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Crear usuario no-root
RUN addgroup -S appuser && adduser -S appuser -G appuser
COPY --chown=appuser:appuser . .
USER appuser
```

2. **Optimización de .dockerignore:**
```
__pycache__/
*.pyc
.git/
.env
README.md
.pytest_cache/
```

### **Lección Aprendida**
Las imágenes Alpine son significativamente más pequeñas que Slim (5MB vs 50MB base), mejorando los tiempos de build y deploy, aunque requieren compilación de dependencias nativas.

---

## Exposición de Secretos en el Repositorio

### **Error Encontrado**
```bash
WARNING: Se encontraron credenciales en el código fuente
SMTP_PASSWORD = "mi_password_real_123"
DB_PASSWORD = "root_password"
```

### **Causa Raíz**
- Archivos .env committeados accidentalmente al repositorio
- Credenciales hardcodeadas en el código Python
- Falta de .gitignore apropiado

### **Solución Aplicada**
1. **Implementación completa de Docker Secrets:**
```yaml
services:
  api:
    secrets:
      - db_password
      - smtp_username  
      - smtp_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

2. **Actualización de .gitignore:**
```
# Environment files
.env
.env.local
.env.*.local

# Secrets
secrets/*.txt
!secrets/*.example
```

3. **Sistema de templates:**
```bash
# secrets/smtp_username.txt.example
tu-email@gmail.com

# secrets/smtp_password.txt.example  
tu-app-password-aqui
```

### **Lección Aprendida**
La seguridad debe implementarse desde el día 1. Usar siempre sistemas de gestión de secretos y nunca commitear credenciales.

---

## Configuración de Nginx y Proxy Reverso

### **Error Encontrado**
```bash
nginx: [emerg] host not found in upstream "api:5000"
502 Bad Gateway
```

### **Causa Raíz**
- Nginx intentaba conectarse a servicios antes de que estuvieran listos
- Configuración incorrecta de upstream en nginx.conf
- Problemas con la red de Docker

### **Solución Aplicada**
1. **Configuración robusta de nginx.conf:**
```nginx
upstream api_backend {
    server api:5000 max_fails=3 fail_timeout=30s;
}

upstream frontend_backend {
    server web:3000 max_fails=3 fail_timeout=30s;
}

location /api/ {
    proxy_pass http://api_backend/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

2. **Health checks para todos los servicios:**
```yaml
api:
  healthcheck:
    test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/')"]
    interval: 15s
    timeout: 8s
    retries: 4
```

### **Lección Aprendida**
Los proxies reversos requieren configuración cuidadosa de timeouts y health checks para manejar la disponibilidad variable de servicios.

---

## Problemas de Dependencias y Puertos

### **Error Encontrado**
```bash
ERROR: Port 3000 is already in use
docker: Error response from daemon: driver failed programming external connectivity
```

### **Causa Raíz**
- Conflictos de puertos con aplicaciones locales
- Servicios de desarrollo corriendo simultáneamente
- Contenedores zombie de ejecuciones anteriores

### **Solución Aplicada**
1. **Script de limpieza automática:**
```bash
#!/bin/bash
# En deploy.sh
echo "Limpiando contenedores existentes..."
docker-compose down --remove-orphans
docker system prune -f

echo "Iniciando servicios..."
docker-compose up -d --build
```

2. **Verificación de puertos:**
```bash
# Verificar puertos disponibles antes del deploy
netstat -tulpn | grep :80
netstat -tulpn | grep :3000
```

3. **Mapeo de puertos flexible:**
```yaml
nginx:
  ports:
    - "${NGINX_PORT:-80}:80"  # Puerto configurable
```

### **Lección Aprendida**
Siempre limpiar el ambiente antes del deploy y usar puertos configurables para evitar conflictos.

---

## Resumen de Errores por Categoría

| Categoría | Errores | Soluciones Clave |
|-----------|---------|------------------|
| **Conectividad** | 3 errores | Health checks, depends_on |
| **Seguridad** | 2 errores | Docker Secrets, .gitignore |
| **Docker** | 4 errores | Multi-stage builds, .dockerignore |
| **Networking** | 2 errores | Nginx config, proxy settings |
| **Configuración** | 3 errores | Scripts de deploy, limpieza automática |

## Mejores Prácticas Adoptadas

1. **Testing Incremental**: Probar cada servicio individualmente antes de la integración completa
2. **Documentación en Tiempo Real**: Registrar errores y soluciones durante el desarrollo
3. **Automatización**: Scripts para deploy, limpieza y verificación automática
4. **Seguridad First**: Implementar gestión de secretos desde el inicio
5. **Health Monitoring**: Health checks en todos los servicios críticos

---