# Documentación de Seguridad - TODO App

Este documento describe las medidas de seguridad implementadas en la aplicación TODO dockerizada, incluyendo la gestión de secretos, escaneos de seguridad y mejores prácticas aplicadas.

## Índice

1. [Gestión de Secretos](#-gestión-de-secretos)
2. [Seguridad en Contenedores](#️-seguridad-en-contenedores)
3. [Escaneos de Seguridad](#-escaneos-de-seguridad)
4. [Mejores Prácticas Aplicadas](#️-mejores-prácticas-aplicadas)
5. [Análisis de Vulnerabilidades](#-análisis-de-vulnerabilidades)

---

## Gestión de Secretos

### **Implementación de Docker Secrets**

La aplicación utiliza **Docker Secrets** para gestionar credenciales sensibles de forma segura, evitando el hardcoding y la exposición en el repositorio.

#### **Secretos Gestionados:**
```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt
  db_root_password:
    file: ./secrets/db_root_password.txt
  flask_secret_key:
    file: ./secrets/flask_secret_key.txt
  smtp_username:
    file: ./secrets/smtp_username.txt
  smtp_password:
    file: ./secrets/smtp_password.txt
```

#### **Estructura de Archivos de Secretos:**
```
secrets/
├── db_password.txt.example         # Template para contraseña de DB
├── db_root_password.txt.example    # Template para root password
├── flask_secret_key.txt.example    # Template para Flask secret key
├── smtp_username.txt.example       # Template para usuario SMTP
├── smtp_password.txt.example       # Template para password SMTP
├── db_password.txt                 # Archivo real (gitignored)
├── db_root_password.txt           # Archivo real (gitignored)
├── flask_secret_key.txt           # Archivo real (gitignored)
├── smtp_username.txt              # Archivo real (gitignored)
└── smtp_password.txt              # Archivo real (gitignored)
```

#### **Lectura Segura de Secretos en Código:**
```python
def read_secret(secret_name):
    """
    Lee secretos de Docker Secrets con fallback a variables de entorno
    """
    try:
        with open(f'/run/secrets/{secret_name}', 'r') as secret_file:
            return secret_file.read().strip()
    except FileNotFoundError:
        # Fallback para desarrollo local
        return os.getenv(secret_name.upper())

# Uso en la aplicación
DB_PASSWORD = read_secret('db_password')
SMTP_USERNAME = read_secret('smtp_username')
```

#### **Configuración de Permisos:**
```bash
# Permisos restrictivos aplicados automáticamente por deploy.sh
chmod 700 secrets/                    # Solo propietario puede acceder
chmod 600 secrets/*.txt              # Solo propietario puede leer/escribir
```

---

## Seguridad en Contenedores

### **Principio de Menor Privilegio**

Todos los contenedores ejecutan con **usuarios no-root** para minimizar el impacto de posibles compromisos de seguridad.

#### **Implementación por Servicio:**

**Backend API (Flask 3.0 + Python 3.11):**
```dockerfile
FROM python:3.11-alpine
# ... configuración ...
RUN addgroup -S appuser && adduser -S appuser -G appuser
USER appuser
EXPOSE 5000
```

**Frontend (React 18 + Nginx 1.25):**
```dockerfile
FROM node:18-alpine as builder
# ... build process ...
FROM nginx:1.25-alpine
RUN addgroup -S nginxgroup && adduser -S nginxuser -G nginxgroup
USER nginxuser
```

**Notificaciones (FastAPI 0.115):**
```dockerfile
FROM python:3.11-slim
# ... setup ...
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
EXPOSE 8001
```

**Base de Datos (MySQL 9.4):**
```dockerfile
FROM mysql:9.4
# Imagen base: todos-db:latest
# Recursos asignados: 2.0 CPU / 1GB RAM (límites)
# Usuario mysql (UID 999) configurado automáticamente
```

### **Imágenes Base Oficiales**

Se utilizan exclusivamente **imágenes base oficiales** para garantizar actualizaciones de seguridad regulares:

- `python:3.11-alpine` - Imagen minimalista de Python (API)
- `python:3.11-slim` - Imagen optimizada de Python (Notifications)
- `node:18-alpine` - Node.js sobre Alpine Linux (imagen ligera)
- `nginx:1.25-alpine` - Nginx sobre Alpine Linux (Web)
- `nginx:1.29-alpine` - Nginx sobre Alpine Linux (Proxy)
- `mysql:9.4` - MySQL oficial con últimas actualizaciones de seguridad

### **Asignación Automática de Recursos de Seguridad**

La aplicación implementa límites de recursos para prevenir ataques DoS y garantizar estabilidad:

```yaml
# Configuración de seguridad por recursos
deploy:
  resources:
    limits:
      cpus: '1.0'        # Previene consumo excesivo de CPU
      memory: 512M       # Limita uso de memoria
      pids: 50          # Limita procesos concurrentes
    reservations:
      cpus: '0.5'        # Garantiza recursos mínimos
      memory: 256M       # Reserva memoria base
```

### **Multi-Stage Builds**

Implementación de **builds multi-etapa** en el servicio Web para reducir la superficie de ataque:

**Frontend React Multi-Stage:**
```dockerfile
# Stage 1: Build de la aplicación React
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Servir con Nginx
FROM nginx:1.25-alpine
RUN apk add --no-cache curl
RUN addgroup -S nginxgroup && adduser -S nginxuser -G nginxgroup
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/nginx/html
RUN chown -R nginxuser:nginxgroup /usr/share/nginx/html
USER nginxuser
```

**Beneficios:**
- Imágenes finales más pequeñas (50-70% reducción de tamaño)
- No incluyen herramientas de build en producción
- Menor superficie de ataque
- Faster deployment y menor uso de ancho de banda

**Nota:** La API usa un enfoque single-stage optimizado con Alpine Linux, que compila dependencias nativas y elimina build-deps en la misma capa, logrando un tamaño similar al multi-stage.

---

### **Configuración de Red Segura**

**Docker Networks:**
```yaml
networks:
  app-network:
    driver: bridge
    name: todos-network
    driver_opts:
      com.docker.network.bridge.name: todos-bridge
      com.docker.network.driver.mtu: 1500
```

**Mapeo de Puertos Restrictivo:**
```yaml
# Solo Nginx expone puertos al host
nginx:
  ports:
    - "80:80"  # Solo puerto HTTP necesario

# Servicios internos NO exponen puertos
api:
  # ports: []  # Sin exposición directa
  expose:
    - "5000"   # Solo accesible internamente
```

---

## Mejores Prácticas Aplicadas

### **1. Gestión de Credenciales**
- **Docker Secrets** para todas las credenciales sensibles
- **Separación de templates** (.example) y archivos reales
- **Exclusión completa** de secretos del repositorio
- **Permisos restrictivos** (600/700) en archivos de secretos

### **2. Hardening de Contenedores**
- **Usuarios no-root** en todos los contenedores
- **Imágenes base oficiales** con actualizaciones regulares
- **Multi-stage builds** para minimizar superficie de ataque
- **Health checks** configurados para todos los servicios

### **3. Seguridad de Red**
- **Proxy reverso (Nginx)** como único punto de entrada
- **Redes Docker isoladas** entre servicios
- **No exposición directa** de servicios backend
- **Headers de seguridad** configurados en Nginx

### **4. Documentación y Monitoreo**
- **Documentación completa** de medidas de seguridad
- **Logs de errores** documentados y solucionados
- **Health monitoring** para detectar problemas temprano
- **Scripts automatizados** para deploy seguro

### **5. DevSecOps**
- **Automatización del deploy** con validaciones de seguridad
- **Cleanup automático** de contenedores y volúmenes
- **Verificación post-deploy** de todos los servicios
- **Rollback capabilities** en caso de problemas

---

## Análisis de Vulnerabilidades

### **Matriz de Riesgos**

| Componente | Riesgo | Nivel | Mitigación Aplicada |
|------------|--------|-------|-------------------|
| **Base de Datos** | Exposición de credenciales | 🔴 Alto | Docker Secrets + usuario no-root |
| **SMTP** | Credenciales en logs | 🟡 Medio | Secrets + app passwords Gmail |
| **Nginx** | Configuración insegura | 🟡 Medio | Headers seguridad + proxy_hide_header |
| **Dependencies** | Vulnerabilidades en paquetes | 🟢 Bajo | Versiones estables + actualizaciones regulares |
| **Network** | Acceso no autorizado | 🟢 Bajo | Redes isoladas + proxy reverso |

---