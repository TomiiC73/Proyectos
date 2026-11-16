# Migración de HTTP a HTTPS con Certificados SSL/TLS

## Índice
1. [Contexto y Motivación](#contexto-y-motivación)
2. [Arquitectura de la Solución](#arquitectura-de-la-solución)
3. [Implementación Técnica](#implementación-técnica)
4. [Configuración de Nginx](#configuración-de-nginx)
5. [Generación de Certificados](#generación-de-certificados)
6. [Parámetros Diffie-Hellman](#parámetros-diffie-hellman)
7. [Despliegue y Persistencia](#despliegue-y-persistencia)
8. [Verificación y Testing](#verificación-y-testing)
9. [Problemas Encontrados](#problemas-encontrados)

---

## Contexto y Motivación

### ¿Por qué HTTPS?

La migración de HTTP a HTTPS fue necesaria por múltiples razones:

1. **Seguridad**: Cifrado de datos en tránsito (TLS 1.2/1.3)
3. **Autenticación**: Verificación de identidad del servidor
4. **Cumplimiento**: Estándares modernos de seguridad web
5. **Confianza**: Navegadores modernos marcan HTTP como "No seguro"

### Estado Inicial (HTTP)

```
Cliente → HTTP:80 → Nginx → API/Web
         ❌ Sin cifrado
         ❌ Datos en texto plano
         ❌ Vulnerable a interceptación
```

### Estado Final (HTTPS)

```
Cliente → HTTPS:443 → Nginx (SSL/TLS) → API/Web
         ✅ Cifrado TLS 1.2/1.3
         ✅ Certificado autofirmado
         ✅ DH params 2048 bits
         ✅ Redirección automática HTTP→HTTPS
```

---

## Arquitectura de la Solución

### Componentes Clave

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENTE (Browser)                     │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              NGINX (Gateway/Proxy)                       │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Puerto 80 (HTTP)                                   │ │
│  │ - Health check: /health → 200 OK                   │ │
│  │ - Todo lo demás: 301 Redirect → HTTPS              │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Puerto 443 (HTTPS)                                 │ │
│  │ - SSL/TLS Termination                              │ │
│  │ - Certificados autofirmados                        │ │
│  │ - DH params (2048 bits)                            │ │
│  │ - Proxy reverso a servicios internos               │ │
│  └────────────────────────────────────────────────────┘ │
└───────┬──────────────────┬────────────────┬─────────────┘
        │                  │                │
        ▼                  ▼                ▼
   ┌─────────┐      ┌──────────┐    ┌──────────────┐
   │   API   │      │   Web    │    │Notifications │
   │  :5000  │      │  :3000   │    │    :8001     │
   └─────────┘      └──────────┘    └──────────────┘
```

### Flujo de Tráfico

1. **Cliente hace request HTTP**:
   ```
   http://172.16.9.31:60180/
   ```

2. **Nginx responde con redirect**:
   ```
   301 Moved Permanently
   Location: https://172.16.9.31:60143/
   ```

3. **Cliente hace request HTTPS**:
   ```
   https://172.16.9.31:60143/
   ```

4. **Nginx termina SSL y proxy a backend**:
   ```
   HTTPS → [Nginx SSL] → HTTP → Backend
   ```

---

## Implementación Técnica

### 1. Dockerfile de Nginx

```dockerfile
FROM nginx:1.27.3-alpine

# Instalar openssl y wget
RUN apk add --no-cache openssl wget

# Copiar configuración
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY entrypoint.sh /docker-entrypoint.d/40-generate-ssl.sh
RUN chmod +x /docker-entrypoint.d/40-generate-ssl.sh

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

**Nota importante**: Nginx Alpine ejecuta automáticamente scripts en `/docker-entrypoint.d/` al iniciar.

---

## Configuración de Nginx

### nginx.conf - Servidor HTTP (Puerto 80)

```nginx
server {
    listen 80;
    server_name _;
    server_tokens off;
    
    # Health check endpoint (no redirect)
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
    
    # Redireccionar todo a HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}
```

**Propósito**:
- **`/health`**: Endpoint especial que NO redirige (para health checks de Docker)
- **`/` (resto)**: Redirección 301 permanente a HTTPS

---

### nginx.conf - Servidor HTTPS (Puerto 443)

```nginx
server {
    server_tokens off;
    listen 443 ssl;
    http2 on;
    resolver 127.0.0.11 valid=30s;
    
    # ============================================
    # SSL CONFIGURATION
    # ============================================
    ssl_certificate /etc/nginx/ssl/nginx-selfsigned.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx-selfsigned.key;
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;
    
    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # ============================================
    # SECURITY HEADERS
    # ============================================
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # ============================================
    # PROXY CONFIGURATION
    # ============================================
    location / {
        proxy_pass http://${WEB_UPSTREAM};
        proxy_set_header X-Forwarded-Proto $scheme;
        # ... más headers ...
    }

    location /api {
        rewrite ^/api(.*)$ $1 break;
        proxy_pass http://${API_UPSTREAM};
        # ... configuración API ...
    }

    location /notifications {
        rewrite ^/notifications/?(.*)$ /$1 break;
        proxy_pass http://${NOTIFICATIONS_UPSTREAM};
        # ... configuración notifications ...
    }
}
```

### Detalles de Configuración SSL

| Directiva | Valor | Propósito |
|-----------|-------|-----------|
| `ssl_protocols` | TLSv1.2 TLSv1.3 | Solo protocolos seguros (no SSLv3, TLS 1.0/1.1) |
| `ssl_ciphers` | HIGH:!aNULL:!MD5 | Cifrados fuertes, sin cifrados nulos o MD5 |
| `ssl_prefer_server_ciphers` | on | El servidor elige el cifrado (más seguro) |
| `ssl_session_cache` | shared:SSL:10m | Cacheo de sesiones SSL (10MB compartido) |
| `ssl_dhparam` | /etc/nginx/ssl/dhparam.pem | Parámetros Diffie-Hellman para Perfect Forward Secrecy |

### Security Headers Explicados

```nginx
# HSTS: Fuerza HTTPS por 1 año (incluye subdominios)
Strict-Transport-Security "max-age=31536000; includeSubDomains"

# Previene clickjacking (solo permite embedding del mismo origen)
X-Frame-Options "SAMEORIGIN"

# Previene MIME-sniffing attacks
X-Content-Type-Options "nosniff"

# Activa filtro XSS del navegador
X-XSS-Protection "1; mode=block"
```

---

## Generación de Certificados

### Entrypoint Script (entrypoint.sh)

Este script se ejecuta **automáticamente** cada vez que el contenedor nginx inicia:

```bash
#!/bin/sh
set -e

SSL_DIR="/etc/nginx/ssl"
mkdir -p "$SSL_DIR"

# ============================================
# GENERAR CERTIFICADO SSL AUTOFIRMADO
# ============================================
if [ ! -f "$SSL_DIR/nginx-selfsigned.crt" ] || [ ! -f "$SSL_DIR/nginx-selfsigned.key" ]; then
    echo "⚠️  Certificados no encontrados - Generando nuevos..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$SSL_DIR/nginx-selfsigned.key" \
        -out "$SSL_DIR/nginx-selfsigned.crt" \
        -subj "/C=AR/ST=Cordoba/L=Cordoba/O=UTN/OU=DevOps/CN=localhost"
    echo "✅ Certificados SSL generados exitosamente"
else
    echo "✅ Certificados SSL ya existen"
fi
```

### Parámetros del Certificado

| Campo | Valor | Descripción |
|-------|-------|-------------|
| `-x509` | | Generar certificado autofirmado (no CSR) |
| `-nodes` | | No cifrar la clave privada (no password) |
| `-days 365` | 1 año | Validez del certificado |
| `-newkey rsa:2048` | RSA 2048 bits | Algoritmo y tamaño de clave |
| `C=AR` | Argentina | País |
| `ST=Cordoba` | Córdoba | Provincia/Estado |
| `L=Cordoba` | Córdoba | Localidad |
| `O=UTN` | | Organización |
| `OU=DevOps` | | Unidad organizativa |
| `CN=localhost` | | Common Name (dominio) |

### Archivos Generados

```
/etc/nginx/ssl/
├── nginx-selfsigned.crt    (Certificado público)
├── nginx-selfsigned.key    (Clave privada)
└── dhparam.pem            (Parámetros Diffie-Hellman)
```

---

## Parámetros Diffie-Hellman

### ¿Qué son los DH params?

Los **parámetros Diffie-Hellman** son números primos grandes usados para **Perfect Forward Secrecy (PFS)**:

- **PFS**: Garantiza que comprometer una clave privada no compromete sesiones pasadas
- **DH**: Permite intercambio seguro de claves sin enviarlas por la red
- **2048 bits**: Mínimo requerido por OpenSSL 3.x (1024 bits rechazado por inseguro)

### Generación de DH Params

```bash
# ============================================
# GENERAR DH PARAMS (2048 bits)
# ============================================
if [ ! -f "$SSL_DIR/dhparam.pem" ]; then
    echo "⚠️  DH params no encontrados - Generando (2048 bits)..."
    echo "   Esto tomará ~2-3 minutos..."
    START_TIME=$(date +%s)
    openssl dhparam -out "$SSL_DIR/dhparam.pem" 2048
    END_TIME=$(date +%s)
    ELAPSED=$((END_TIME - START_TIME))
    echo "✅ DH params generados en ${ELAPSED}s"
else
    echo "✅ DH params ya existen"
fi
```

### Tiempo de Generación

| Bits | Tiempo aprox. | Seguridad | OpenSSL 3.x |
|------|---------------|-----------|-------------|
| 1024 | ~30 segundos  | ❌ Baja   | ❌ Rechazado |
| 2048 | ~2-3 minutos  | ✅ Alta   | ✅ Aceptado |
| 4096 | ~10-15 minutos | ✅ Muy alta | ✅ Aceptado |

**Decisión**: Usamos **2048 bits** por balance entre seguridad y tiempo de deploy.

---

## Despliegue y Persistencia

### docker-compose.yml - Volumen SSL

```yaml
services:
  nginx:
    image: registry-alumnos.labsis.frc.utn.edu.ar:8443/todos-nginx:latest
    container_name: todos-nginx
    ports:
      - "60180:80"    # HTTP
      - "60143:443"   # HTTPS
    volumes:
      - nginx_ssl:/etc/nginx/ssl  # ⭐ Persistir certificados
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost/health || exit 1"]
      interval: 15s
      timeout: 10s
      retries: 5
      start_period: 60s

volumes:
  nginx_ssl:
    driver: local
    name: todos-nginx-ssl
```

### ¿Por qué persistir el volumen?

```bash
# SIN volumen persistente:
docker compose down
# → Certificados y DH params SE PIERDEN
# → Próximo deploy: regenerar todo (~3 minutos)

# CON volumen persistente:
docker compose down
# → Volumen nginx_ssl se MANTIENE
# → Próximo deploy: reutiliza certificados (~5 segundos)
```

### Pipeline GitLab CI/CD - Deploy

```yaml
deploy:production:
  script:
    # Limpiar contenedores pero NO volúmenes
    - docker compose down --remove-orphans || true
    
    # Limpiar SOLO el volumen SSL (forzar regeneración)
    - docker volume rm todos-nginx-ssl || true
    
    # Eliminar dhparam viejo (si existe)
    - docker run --rm -v todos-nginx-ssl:/ssl alpine sh -c "rm -f /ssl/dhparam.pem" || true
    
    # Iniciar servicios
    - docker compose up -d
    
    # Esperar 3 minutos para generación de dhparam
    - echo "Esperando 3 minutos para generación de DH params (2048 bits)..."
    - sleep 180
    
    # Health check de HTTPS
    - |
      MAX_ATTEMPTS=20
      ATTEMPT=0
      until curl -s -k -f https://172.16.9.31:60143 > /dev/null 2>&1; do
        ATTEMPT=$((ATTEMPT+1))
        if [ "$ATTEMPT" -ge "$MAX_ATTEMPTS" ]; then
          echo "ERROR: Timeout esperando respuesta HTTPS"
          exit 1
        fi
        sleep 3
      done
```

### Estrategia de Deploy

1. **Limpiar dhparam viejo**: Forzar regeneración con 2048 bits
2. **Esperar 180 segundos**: Dar tiempo para generación de DH params
3. **Health check incremental**: Verificar cada 3 segundos (máx 60s)
4. **Usar `-k` en curl**: Aceptar certificados autofirmados

---

## Verificación y Testing

### 1. Verificar Certificados en Contenedor

```bash
# Ingresar al contenedor nginx
docker exec -it todos-nginx sh

# Verificar archivos SSL
ls -lh /etc/nginx/ssl/
# Output esperado:
# nginx-selfsigned.crt  (1.3K)
# nginx-selfsigned.key  (1.7K)
# dhparam.pem          (424 bytes = 2048 bits)

# Ver información del certificado
openssl x509 -in /etc/nginx/ssl/nginx-selfsigned.crt -noout -subject -dates
# Output:
# subject=C=AR, ST=Cordoba, L=Cordoba, O=UTN, OU=DevOps, CN=localhost
# notBefore=Nov 27 12:00:00 2025 GMT
# notAfter=Nov 27 12:00:00 2026 GMT

# Verificar tamaño de DH params
openssl dhparam -in /etc/nginx/ssl/dhparam.pem -text -noout | grep "DH Parameters"
# Output: DH Parameters: (2048 bit)
```

### 2. Testear Redirección HTTP → HTTPS

```bash
# Hacer request HTTP
curl -I http://172.16.9.31:60180/

# Output esperado:
HTTP/1.1 301 Moved Permanently
Server: nginx
Location: https://172.16.9.31:60180/
```

### 3. Testear HTTPS

```bash
# Request HTTPS (aceptar certificado autofirmado)
curl -k https://172.16.9.31:60143/

# Output: HTML del frontend React
```

### 4. Verificar Headers de Seguridad

```bash
curl -k -I https://172.16.9.31:60143/ | grep -E "Strict|X-Frame|X-Content|X-XSS"

# Output esperado:
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

### 5. Verificar Protocolo SSL/TLS

```bash
openssl s_client -connect 172.16.9.31:60143 -tls1_2

# Output (fragmento):
Protocol  : TLSv1.2
Cipher    : ECDHE-RSA-AES256-GCM-SHA384
```

### 6. Job de Verificación en Pipeline

```yaml
verify:deployment:
  script:
    - echo "SSL Certificate Info (nginx container volume):"
    - |
      docker exec todos-nginx sh -c '
        if [ -f "/etc/nginx/ssl/server.crt" ]; then
          openssl x509 -in /etc/nginx/ssl/server.crt -noout -subject -dates
          echo "✓ Certificado SSL generado por nginx entrypoint"
          echo "DH params:"
          ls -lh /etc/nginx/ssl/dhparam.pem 2>/dev/null || echo "⚠ dhparam.pem no encontrado"
        fi
      '
```

---

## Problemas Encontrados

### 1. Error: DH Key Too Small

**Síntoma**:
```
SSL_CTX_set_tmp_dh("/etc/nginx/ssl/dhparam.pem") failed 
(SSL: error:0A00018A:SSL routines::dh key too small)
```

**Causa**: OpenSSL 3.x rechaza DH params menores a 2048 bits.

**Solución**:
```bash
# Cambiar de 1024 a 2048 bits
openssl dhparam -out "$SSL_DIR/dhparam.pem" 2048
```

**Ver**: [ERRORES.md - Error #4](./ERRORES.md#4-error-nginx-timeout-durante-despliegue)

---

### 2. Error: Nginx Timeout Durante Deploy

**Síntoma**:
```
Error: nginx container timeout (300s exceeded)
```

**Causa**: Generación de DH params 2048 bits tarda 2-3 minutos.

**Solución**:
```yaml
# Aumentar tiempo de espera a 3 minutos
- sleep 180
```

**Ver**: [ERRORES.md - Error #4](./ERRORES.md#4-error-nginx-timeout-durante-despliegue)

---

### 3. Warning: http2 Directive Deprecated

**Síntoma**:
```
nginx: [warn] the "listen ... http2" directive is deprecated, 
use the "http2" directive instead
```

**Solución**:
```nginx
# Antes (deprecated):
listen 443 ssl http2;

# Después (correcto):
listen 443 ssl;
http2 on;
```

---

### 4. Error: Health Check Fallando en Puerto 80

**Síntoma**:
```
todos-nginx    Up 3 minutes (unhealthy)
```

**Causa**: Todo el tráfico HTTP redirige a HTTPS (301), pero health check esperaba 200.

**Solución**:
```nginx
# Agregar endpoint especial que NO redirige
location /health {
    access_log off;
    return 200 "OK\n";
    add_header Content-Type text/plain;
}
```

**Ver**: [ERRORES.md - Error #6](./ERRORES.md#6-error-nginx-unhealthy---health-check-fallando)

---

## Diagrama de Flujo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    INICIO: docker compose up                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│         Nginx Container Inicia                                   │
│         Ejecuta: /docker-entrypoint.d/40-generate-ssl.sh         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ ¿Existen certs? │
                    └────┬──────┬────┘
                         │ NO   │ SI
                         ▼      ▼
              ┌─────────────┐  ┌──────────────────┐
              │ Generar     │  │ Reutilizar certs │
              │ certificados│  │ existentes       │
              │ (~5 seg)    │  │ (~1 seg)         │
              └──────┬──────┘  └────────┬─────────┘
                     │                  │
                     └────────┬─────────┘
                              ▼
                    ┌────────────────────┐
                    │ ¿Existe dhparam?   │
                    └────┬──────┬────────┘
                         │ NO   │ SI
                         ▼      ▼
              ┌─────────────┐  ┌──────────────────┐
              │ Generar     │  │ Reutilizar       │
              │ dhparam     │  │ dhparam          │
              │ (~2-3 min)  │  │ (~1 seg)         │
              └──────┬──────┘  └────────┬─────────┘
                     │                  │
                     └────────┬─────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Nginx Config Validation (nginx -t)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Nginx Inicia: daemon off                            │
│              - Puerto 80: HTTP (redirect + /health)              │
│              - Puerto 443: HTTPS (SSL termination)               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Health Check: wget http://localhost/health          │
│              Resultado: 200 OK → Container healthy               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Resumen de Archivos Modificados

| Archivo | Propósito |
|---------|-----------|
| `nginx/Dockerfile` | Instalar openssl, copiar entrypoint |
| `nginx/entrypoint.sh` | Generar certificados y DH params al iniciar |
| `nginx/nginx.conf` | Configuración HTTP→HTTPS, SSL/TLS, proxy |
| `docker-compose.yml` | Volumen `nginx_ssl`, puertos 80/443 |
| `.gitlab/ci/deploy-gitlab-ci.yml` | Espera 180s, health check HTTPS |

---

## Conclusión

La migración a HTTPS se implementó con:

✅ **Certificados autofirmados** generados automáticamente  
✅ **DH params 2048 bits** para Perfect Forward Secrecy  
✅ **TLS 1.2/1.3** con cifrados fuertes  
✅ **Security headers** (HSTS, X-Frame-Options, etc.)  
✅ **Redirección automática** HTTP → HTTPS  
✅ **Persistencia** de certificados mediante volúmenes  
✅ **Health checks** compatibles con HTTP y HTTPS  
✅ **Deploy optimizado** con tiempos de espera adecuados  

**Resultado**: Aplicación completamente funcional sobre HTTPS con certificados autofirmados, lista para producción con certificados válidos (Let's Encrypt, etc.).
