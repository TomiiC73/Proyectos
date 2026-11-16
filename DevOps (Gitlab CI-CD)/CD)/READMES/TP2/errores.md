# Glosario de Errores y Soluciones

## 1. Error: Pipeline con más de 1100 líneas difícil de mantener

### Identificación
El archivo `.gitlab-ci.yml` original tenía más de 1100 líneas, haciéndolo extremadamente difícil de leer, mantener y depurar.

### Solución
**Modularización del pipeline** en múltiples archivos:
- `.gitlab-ci.yml`: Archivo principal (75 líneas)
- `.gitlab/template/templates.yml`: Templates reutilizables
- `.gitlab/template/rules.yml`: Reglas de ejecución
- `.gitlab/ci/*.yml`: Jobs organizados por stage (7 archivos)

**Resultado**: Pipeline organizado, mantenible y fácil de extender.

---

## 2. Error: YAML syntax error - "Unknown alias"

### Identificación
```
yaml invalid: jobs:build:api config should contain a script: keyword or a trigger: keyword
```

### Causa
Uso incorrecto de anchors (`&template`) y aliases (`*template`) a través de archivos incluidos con `include:`.

### Solución
Reemplazar anchors/aliases por la palabra clave `extends`:

**Antes (❌ No funciona)**:
```yaml
.base_template: &template
  script:
    - echo "test"

job1:
  <<: *template
```

**Después (✅ Funciona)**:
```yaml
.base_template:
  script:
    - echo "test"

job1:
  extends: .base_template
```

---

## 3. Error: "config should be a string or nested array of strings"

### Identificación
```
jobs:lint:python:flake8 config should be a string or a nested array of strings up to 10 levels deep
```

### Causa
Comentarios inline dentro de arrays en YAML.

**Código problemático**:
```yaml
script:
  - echo "step 1"  # Este comentario causa error
  - echo "step 2"
```

### Solución
- Mover comentarios fuera de los arrays
- Usar bloques multilínea (`|`) cuando sea necesario

**Corregido**:
```yaml
# Paso 1: Preparar entorno
script:
  - echo "step 1"
  - echo "step 2"
```

---

## 4. Error: Nginx timeout durante despliegue

### Identificación
```
Error: nginx container timeout (300s exceeded)
SSL_CTX_set_tmp_dh("/etc/nginx/ssl/dhparam.pem") failed (SSL: error:0A00018A:SSL routines::dh key too small)
```

### Causa
Generación de parámetros Diffie-Hellman de 2048 bits tardaba 2-3 minutos, excediendo el timeout de health check inicial (45 segundos). Además, OpenSSL moderno requiere **mínimo 2048 bits** para DH params (1024 bits fue rechazado por ser inseguro).

### Solución
1. **Mantener DH params en 2048 bits** (requerido por OpenSSL 3.x):
```bash
openssl dhparam -out dhparam.pem 2048
```

2. **Aumentar tiempo de espera** en deploy a 3 minutos:
```yaml
# deploy-gitlab-ci.yml
- echo "Esperando a que los contenedores estén listos (3 min para dhparam)..."
- sleep 180
```

3. **Limpiar dhparam antiguo** antes de deploy:
```bash
docker run --rm -v todos-nginx-ssl:/ssl alpine sh -c "rm -f /ssl/dhparam.pem" || true
```

4. **Verificar si ya existen** antes de generar:
```bash
if [ ! -f "$SSL_DIR/dhparam.pem" ]; then
    echo "Generando parámetros Diffie-Hellman (2048 bits, ~2-3 minutos)..."
    openssl dhparam -out "$SSL_DIR/dhparam.pem" 2048
fi
```

5. **Persistir volumen** entre deploys:
```yaml
volumes:
  nginx_ssl:
    driver: local
    name: todos-nginx-ssl
```

**Nota de seguridad**: No reducir a 1024 bits ya que OpenSSL 3.x lo rechaza por ser inseguro. El tiempo de generación de 2-3 minutos es aceptable para la seguridad que proporciona.

---

## 5. Error: Docker secrets - PermissionError

### Identificación
```python
PermissionError: [Errno 13] Permission denied: '/run/secrets/flask_secret_key'
```

### Causa
Permisos restrictivos (600) en archivos de secrets montados por Docker.

### Solución
1. **Cambiar permisos a 644**:
```bash
chmod 644 secrets/*.txt
```

2. **Implementar fallback** en el código:
```python
# Prioridad: archivo secret → variable entorno → default
secret_key_file = os.getenv('SECRET_KEY_FILE')
if secret_key_file and os.path.exists(secret_key_file):
    try:
        with open(secret_key_file, 'r') as f:
            SECRET_KEY = f.read().strip()
    except (PermissionError, IOError):
        SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-key')
else:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-key')
```

---

## 6. Error: Nginx unhealthy - Health check fallando

### Identificación
```
todos-nginx    Up 3 minutes (unhealthy)
```

### Causa raíz
El puerto 80 redirige todo a HTTPS (301), pero el health check esperaba 200 OK.

```bash
wget http://localhost/
# Devuelve 301 → Health check falla
```

### Solución
Agregar endpoint `/health` que **no redirige**:

```nginx
server {
    listen 80;
    
    # Health check endpoint (no redirect)
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
    
    location / {
        return 301 https://$host$request_uri;
    }
}
```

Health check actualizado:
```yaml
healthcheck:
  test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost/health || exit 1"]
```

---

## 7. Error: Conexión a base de datos falla

### Identificación
```python
{"error":"Error de conexión a la base de datos"}
```

### Causa
- Host por defecto: `localhost` (incorrecto en Docker)
- Usuario por defecto: `root` (debería ser `todos_user`)
- Sin retry automático

### Solución
1. **Cambiar defaults** en `db_config.py`:
```python
db_host = os.getenv('DB_HOST', 'db')  # Nombre del contenedor
db_user = os.getenv('DB_USER', 'todos_user')
```

2. **Implementar retry automático**:
```python
for attempt in range(1, 6):
    try:
        connection = mysql.connector.connect(...)
        return connection
    except mysql.connector.Error:
        if attempt < 5:
            time.sleep(2)
```

3. **Esperar a que BD esté healthy**:
```yaml
api:
  depends_on:
    db:
      condition: service_healthy
```

---

## 8. Error: Variables de entorno no se leen

### Identificación
Valores "NOT SET" en logs de configuración.

### Causa
Archivos `.env` no existían cuando se referenciaban en `docker-compose.yml`.

### Solución
El script de deploy crea los `.env` dinámicamente desde variables de GitLab CI/CD:

```bash
cat > api/.env << EOF
DB_HOST=db
DB_USER=${MYSQL_USER}
DB_PASSWORD=${DB_PASSWORD}
EOF
```

---

## 9. Error: Curl vs Wget en Alpine Linux

### Identificación
```
/bin/sh: curl: not found
```

### Causa
Imágenes Alpine no incluyen `curl` por defecto, solo `wget`.

### Solución
1. **Usar wget** en health checks:
```dockerfile
RUN apk add --no-cache wget
HEALTHCHECK CMD wget --spider http://localhost/health
```

2. O instalar curl si es necesario:
```dockerfile
RUN apk add --no-cache curl
```

---

## 10. Error: API devuelve 404 en /health

### Identificación
```
GET /api/health - Status: 404
```

### Causa
Endpoint `/health` agregado al código pero imagen Docker no reconstruida.

### Solución
1. Hacer commit del código
2. Dejar que el pipeline reconstruya la imagen
3. Deploy automático actualiza el contenedor

---

## 11. Error: Bash syntax error en heredocs con comentarios inline

### Identificación
```bash
línea 229: % 5: error sintáctico: se esperaba un operando
documento-aquí en la línea 229 está delimitado por fin-de-fichero (se esperaba `EOF')
basename: falta un operando
```

### Causa
Comentarios inline con caracteres especiales (tildes: á, é, í, ó, ú; símbolos: %, *, etc.) dentro de heredocs y bloques bash en archivos YAML causaban errores de parsing.

**Código problemático**:
```yaml
script:
  - |
    cat > api/.env << EOF
    DB_HOST=db  # Host de la base de datos
    DB_USER=${MYSQL_USER}  # Usuario con tildes: configuración
    DB_PASSWORD=${DB_PASSWORD}  # Contraseña desde variable CI/CD
    EOF
  - |
    for i in $(seq 1 20); do  # Intentar 20 veces
      if [ $((i % 5)) -eq 0 ]; then  # Cada 5 intentos → Error aquí
        echo "Intento $i..."
      fi
    done
```

**Error específico**: Bash interpreta `%` en comentarios dentro de heredocs como parte del código, causando errores de sintaxis.

### Solución
**Eliminar TODOS los comentarios inline** de líneas ejecutables en bloques bash:

```yaml
script:
  # Crear archivo .env para la API
  - |
    cat > api/.env << EOF
    DB_HOST=db
    DB_USER=${MYSQL_USER}
    DB_PASSWORD=${DB_PASSWORD}
    EOF
  
  # Health check cada 5 intentos durante 20 rondas
  - |
    for i in $(seq 1 20); do
      if [ $((i % 5)) -eq 0 ]; then
        echo "Intento $i..."
      fi
    done
```

**Regla**: Solo usar comentarios **fuera** de bloques ejecutables. Dentro de heredocs, scripts multilínea o comandos complejos, **nunca** usar comentarios inline.

### Lección aprendida
- Bash en YAML es especialmente sensible a comentarios
- Los caracteres especiales (%, *, tildes) en comentarios causan parsing ambiguo
- Preferir comentarios de sección sobre comentarios inline en scripts
- Heredocs (`<< EOF`) son zonas de alto riesgo para comentarios

---

## Lecciones Aprendidas

1. **Modularizar desde el inicio**: Archivos grandes son imposibles de mantener
2. **YAML es sensible**: No usar comentarios inline, cuidado con indentación
3. **Secrets con fallback**: Siempre tener plan B para leer configuración
4. **Health checks específicos**: No asumir que `curl /` funciona
5. **Docker networking**: Usar nombres de servicios, no `localhost`
6. **Retry automático**: Especialmente para conexiones de BD
7. **Persistir volúmenes**: Evitar regenerar SSL certs en cada deploy
8. **Alpine vs Debian**: Conocer diferencias en paquetes disponibles
9. **Logging verboso**: Fundamental para debugging en CI/CD
10. **Test en producción**: Automatizar verificación post-deploy
