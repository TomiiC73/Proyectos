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

# Errores de la Parte 2 - CI/CD Pipeline

## Índice de Errores Parte 2

1. [Error de Variables de GitLab CI/CD](#-error-de-variables-de-gitlab-cicd)
2. [Problemas con Artefactos HTML](#-problemas-con-artefactos-html)
3. [Timeout en Build de Imágenes](#-timeout-en-build-de-imágenes)
4. [Error de Autenticación en Registry](#-error-de-autenticación-en-registry)
5. [Conflictos en Hadolint](#-conflictos-en-hadolint)
6. [Problemas de Permisos SSH](#-problemas-de-permisos-ssh)
7. [Certificados SSL Auto-generados](#-certificados-ssl-auto-generados)

---

## Error de Variables de GitLab CI/CD

### **Error Encontrado**
```bash
ERROR: Job failed: exit code 1
docker login: Error response from daemon: Get https://$REGISTRY_URL/v2/: unauthorized
```

### **Causa Raíz**
- Variables de CI/CD no configuradas en GitLab
- Variables protegidas no disponibles en branches no protegidas
- Sintaxis incorrecta para referenciar variables

### **Solución Aplicada**

1. **Configurar variables en GitLab:**
   - Settings → CI/CD → Variables
   - Agregar cada variable como "Protected" y "Masked" cuando corresponda:
     - `REGISTRY_URL`
     - `REGISTRY_USER`
     - `REGISTRY_PASSWORD` (masked)
     - `DEPLOY_HOST`
     - `DEPLOY_USER`
     - `DEPLOY_SSH_KEY` (file type, protected)

2. **Verificar sintaxis en .gitlab-ci.yml:**
```yaml
variables:
  # Uso correcto de variables
  REGISTRY_URL: $REGISTRY_URL
  IMAGE_TAG: $CI_COMMIT_SHORT_SHA
```

3. **Proteger la branch main:**
   - Settings → Repository → Protected Branches
   - Agregar `main` como protected branch

### **Lección Aprendida**
Las variables protegidas solo están disponibles en branches protegidas. Configurar correctamente los permisos de las variables según la seguridad requerida.

---

## Problemas con Artefactos HTML

### **Error Encontrado**
```bash
# detect-secrets no genera HTML nativamente
ERROR: detect-secrets does not support HTML output format
```

### **Causa Raíz**
- `detect-secrets` solo soporta formatos JSON y texto plano
- Expectativa de reportes HTML para todas las herramientas

### **Solución Aplicada**

1. **Usar herramientas con soporte HTML:**
```yaml
# Bandit con formato HTML
bandit -r . -f html -o ../bandit-api-report.html

# Flake8 con plugin HTML
flake8 . --format=html --htmldir=../flake8-api-report

# ESLint con formato HTML
npx eslint src/ --format html --output-file ../eslint-web-report.html
```

2. **Para detect-secrets, usar formato texto:**
```yaml
secrets-scan:api:
  script:
    - detect-secrets scan api/ --baseline .secrets.baseline || true
    - detect-secrets audit .secrets.baseline > secrets-api-report.txt || true
  artifacts:
    paths:
      - secrets-api-report.txt
```

3. **Considerar conversión post-proceso:**
```bash
# Convertir JSON a HTML con jq y template
cat report.json | jq -r '.' | python convert_to_html.py > report.html
```

### **Lección Aprendida**
No todas las herramientas soportan todos los formatos. Investigar las capacidades de cada herramienta antes de definir requisitos de artefactos.

---

## Timeout en Build de Imágenes

### **Error Encontrado**
```bash
ERROR: Job failed: execution took longer than 1h0m0s seconds
```

### **Causa Raíz**
- Instalación de dependencias muy lenta
- Sin cache de layers de Docker
- Runners con recursos limitados
- Reinstalación completa en cada build

### **Solución Aplicada**

1. **Optimizar Dockerfiles:**
```dockerfile
# Orden óptimo de instrucciones para aprovechar cache
FROM python:3.11-alpine

# 1. Copiar solo requirements primero
COPY requirements.txt .

# 2. Instalar dependencias (esta layer se cachea)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar código (cambia frecuentemente, no invalida cache anterior)
COPY . .
```

2. **Usar cache en GitLab CI:**
```yaml
build:api:
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .docker-cache/
  script:
    - docker build --cache-from $API_IMAGE:latest -t $API_IMAGE:$IMAGE_TAG ./api
```

3. **Pull de imagen anterior como cache:**
```yaml
before_script:
  - docker pull $API_IMAGE:latest || true
script:
  - docker build --cache-from $API_IMAGE:latest -t $API_IMAGE:$IMAGE_TAG ./api
```

4. **Incrementar timeout del job:**
```yaml
build:api:
  timeout: 2h
```

### **Lección Aprendida**
El cache de Docker layers es fundamental para builds rápidos. Optimizar el orden de instrucciones en Dockerfile y usar `--cache-from` para aprovechar builds anteriores.

---

## Error de Autenticación en Registry

### **Error Encontrado**
```bash
Error response from daemon: login attempt to https://registry.labsis.com/v2/ failed with status: 401 Unauthorized
```

### **Causa Raíz**
- Credenciales incorrectas en variables de CI/CD
- Formato incorrecto de la URL del registry
- Token expirado o revocado

### **Solución Aplicada**

1. **Verificar formato de URL:**
```yaml
# Incorrecto
REGISTRY_URL: https://registry.labsis.com

# Correcto
REGISTRY_URL: registry.labsis.com
```

2. **Usar docker login correctamente:**
```yaml
before_script:
  - echo "$REGISTRY_PASSWORD" | docker login -u "$REGISTRY_USER" --password-stdin "$REGISTRY_URL"
```

3. **Verificar credenciales manualmente:**
```bash
# Probar login localmente
docker login registry.labsis.com -u username -p password
```

4. **Usar token de acceso si está disponible:**
```yaml
before_script:
  - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
```

### **Lección Aprendida**
Siempre verificar credenciales y formato de URL del registry. Usar `--password-stdin` para evitar exponer passwords en logs.

---

## Conflictos en Hadolint

### **Error Encontrado**
```bash
DL3018 warning: Pin versions in apk add
DL3059 info: Multiple consecutive RUN instructions
```

### **Causa Raíz**
- Hadolint es muy estricto con mejores prácticas
- Algunos warnings son inevitables en ciertos contextos
- Dockerfile optimizados para tamaño vs. mejores prácticas

### **Solución Aplicada**

1. **Usar ignore para reglas específicas:**
```dockerfile
# hadolint ignore=DL3018
RUN apk add --no-cache curl gettext openssl
```

2. **Configurar hadolint:**
```yaml
# .hadolint.yaml
ignored:
  - DL3018  # Pin versions en apk (versiones cambian frecuentemente)
  - DL3059  # Multiple RUN (necesario para multi-stage)
```

3. **Permitir que el job continúe:**
```yaml
docker-lint:api:
  script:
    - hadolint api/Dockerfile || true  # No fallar el pipeline
  allow_failure: true
```

4. **Balancear entre advertencias y pragmatismo:**
```dockerfile
# Mejor: combinar RUN cuando sea posible
RUN apk update \
    && apk add --no-cache curl \
    && rm -rf /var/cache/apk/*
```

### **Lección Aprendida**
El linting es una guía, no una ley absoluta. Usar `allow_failure: true` para jobs de linting que no deben bloquear el pipeline.

---

## Problemas de Permisos SSH

### **Error Encontrado**
```bash
Warning: Permanently added 'host' (ECDSA) to the list of known hosts.
Permission denied (publickey).
```

### **Causa Raíz**
- SSH key no cargada correctamente en ssh-agent
- Permisos incorrectos en la clave privada
- Host key no aceptada automáticamente

### **Solución Aplicada**

1. **Configurar SSH agent correctamente:**
```yaml
before_script:
  - apk add --no-cache openssh-client
  - eval $(ssh-agent -s)
  - echo "$DEPLOY_SSH_KEY" | tr -d '\r' | ssh-add -
  - mkdir -p ~/.ssh
  - chmod 700 ~/.ssh
  - ssh-keyscan -H $DEPLOY_HOST >> ~/.ssh/known_hosts
```

2. **Formato de variable SSH_KEY:**
```bash
# La variable debe contener la clave COMPLETA con saltos de línea
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
...
-----END RSA PRIVATE KEY-----
```

3. **Variable de tipo File:**
   - En GitLab: Settings → CI/CD → Variables
   - Tipo: "File" (no "Variable")
   - Esto crea un archivo temporal automáticamente

4. **Alternativa con archivo temporal:**
```yaml
before_script:
  - echo "$DEPLOY_SSH_KEY" > /tmp/deploy_key
  - chmod 600 /tmp/deploy_key
  - ssh -i /tmp/deploy_key $DEPLOY_USER@$DEPLOY_HOST "command"
```

### **Lección Aprendida**
Las claves SSH requieren formato exacto y permisos correctos. Usar variables de tipo "File" en GitLab simplifica la gestión de keys.

---

## Certificados SSL Auto-generados

### **Error Encontrado**
```bash
curl: (60) SSL certificate problem: self signed certificate
```

### **Causa Raíz**
- Certificados self-signed no son confiados por defecto
- Navegadores y herramientas rechazan certificados auto-firmados
- Necesidad de bypass para desarrollo

### **Solución Aplicada**

1. **Generar certificados en entrypoint:**
```bash
#!/bin/sh
SSL_DIR="/etc/nginx/ssl"
mkdir -p "$SSL_DIR"

if [ ! -f "$SSL_DIR/nginx-selfsigned.crt" ]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$SSL_DIR/nginx-selfsigned.key" \
        -out "$SSL_DIR/nginx-selfsigned.crt" \
        -subj "/C=AR/ST=Cordoba/L=Cordoba/O=UTN/OU=DevOps/CN=localhost"
    
    openssl dhparam -out "$SSL_DIR/dhparam.pem" 2048
fi
```

2. **Configurar nginx para SSL:**
```nginx
server {
    listen 443 ssl http2;
    
    ssl_certificate /etc/nginx/ssl/nginx-selfsigned.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx-selfsigned.key;
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

3. **Bypass en desarrollo con curl:**
```bash
# -k ignora validación de certificado
curl -k https://localhost/health
```

4. **Health check con certificado self-signed:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "-k", "https://localhost/health"]
```

5. **Nota para producción:**
```yaml
# Para producción, usar Let's Encrypt:
# certbot certonly --standalone -d yourdomain.com
# Copiar certificados a volumen Docker
```

### **Lección Aprendida**
Los certificados self-signed son adecuados para desarrollo pero no para producción. Usar Let's Encrypt o CA válida en ambientes productivos.

---

## Resumen de Errores Parte 2

| Categoría | Errores | Soluciones Clave |
|-----------|---------|------------------|
| **CI/CD Config** | 3 errores | Variables protegidas, branch protection |
| **Build/Deploy** | 2 errores | Cache de Docker, timeout aumentado |
| **Autenticación** | 2 errores | Formato correcto de credenciales, SSH agent |
| **Linting** | 1 error | allow_failure, configuración hadolint |
| **SSL/TLS** | 1 error | Certificados self-signed, bypass en desarrollo |

## Lecciones Generales de la Parte 2

1. **Pipeline como Código**: El .gitlab-ci.yml es código y debe tratarse como tal (versionado, review, testing)
2. **Fail Fast, Fail Safe**: Los jobs deben fallar rápido pero no bloquear innecesariamente
3. **Artefactos son Documentación**: Los reportes generados documentan la calidad del código
4. **Seguridad en Layers**: Múltiples capas de validación atrapan más problemas
5. **Automatización Pragmática**: Automatizar lo repetible, manual lo crítico

---

**Documento actualizado**: 19 de noviembre de 2025 - Parte 2 completada