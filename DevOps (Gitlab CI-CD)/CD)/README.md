# DevOps - CI/CD con GitLab

Aplicación TODO con pipeline completo de CI/CD en GitLab. Implementa integración y despliegue continuo con múltiples stages de validación, seguridad y testing.

## 📋 Descripción

Evolución del proyecto Docker que incorpora un pipeline completo de CI/CD con GitLab. El proyecto implementa las mejores prácticas de DevOps incluyendo análisis de seguridad, escaneo de vulnerabilidades, linting de código y despliegue automatizado.

## 🏗️ Arquitectura

Misma arquitectura de microservicios que el proyecto Docker, pero con la adición de:
- Pipeline de CI/CD automatizado
- HTTPS configurado en todos los servicios
- Headers de seguridad mejorados
- Health checks implementados
- Tests de producción automatizados

## 🔄 Pipeline CI/CD

El pipeline consta de **8 stages** automatizados:

1. **Secrets Scan** - Detección de secretos con `detect-secrets`
2. **Code Lint** - Análisis de código (flake8, pylint, eslint)
3. **Docker Lint** - Validación de Dockerfiles con `hadolint`
4. **IaC Scan** - Escaneo de infraestructura con `Checkov`
5. **Build** - Construcción de imágenes Docker
6. **Image Scan** - Escaneo de vulnerabilidades con `Trivy`
7. **Deploy** - Despliegue por SSH
8. **Production Tests** - Tests de endpoints y health checks

## 🔧 Tecnologías

### Aplicación
- Docker, Docker Compose
- React, Flask, FastAPI
- MySQL, Nginx

### CI/CD y Seguridad
- **CI/CD:** GitLab CI/CD
- **Escaneo de Secretos:** detect-secrets
- **Code Linting:** flake8, pylint, eslint
- **Docker Linting:** hadolint
- **IaC Scanning:** Checkov
- **Vulnerability Scanning:** Trivy
- **HTTPS:** Certificados SSL/TLS

## 🚀 Ejecución Local

```bash
# Levantar servicios con docker-compose
docker-compose up -d

# Acceder a la aplicación (con HTTPS)
https://localhost
```

## 🔐 Seguridad Implementada

- ✅ Sin secretos hardcodeados
- ✅ Variables de GitLab (Protected + Masked)
- ✅ Docker Secrets para credenciales
- ✅ HTTPS en todos los puertos
- ✅ Headers de seguridad en Nginx (HSTS, X-Frame-Options, CSP)
- ✅ Escaneo continuo de vulnerabilidades
- ✅ Análisis estático de código

## 📊 Artefactos del Pipeline

Cada stage genera artefactos con los resultados:
- Reportes de escaneo de secretos
- Reportes de linting
- Reportes de vulnerabilidades (JSON y HTML)
- Logs de build
- Resultados de tests de producción

## 📚 Documentación Detallada

### TP1 (Base Docker)
- [README](./READMES/TP1/README.md)
- [Errores](./READMES/TP1/ERRORES.md)
- [Seguridad](./READMES/TP1/SEGURIDAD.md)
- [Secretos](./READMES/TP1/SECRETS.md)

### TP2 (CI/CD)
- [Pipeline](./READMES/TP2/pipeline.md) - Documentación completa del pipeline con capturas
- [HTTPS](./READMES/TP2/HTTPS.md) - Configuración de certificados SSL/TLS
- [Health Checks](./READMES/TP2/health-checks.md) - Implementación de health checks
- [Errores](./READMES/TP2/errores.md) - Solución de problemas del pipeline
- [Conclusiones](./READMES/TP2/conclusiones.md) - Logros y mejoras propuestas

## 📁 Estructura

```
.gitlab/
  ci/                    - Archivos de configuración del pipeline
  template/              - Templates y reglas reutilizables
  templates/             - Templates de reportes
api/                     - Servicio Flask (Backend)
web/                     - Servicio React (Frontend)
notifications/           - Servicio FastAPI
db/                      - Configuración MySQL
nginx/                   - Proxy reverso con HTTPS
READMES/                 - Documentación completa (TP1 y TP2)
secrets-examples/        - Ejemplos de archivos de secretos
.gitlab-ci.yml          - Pipeline principal (modular, ~75 líneas)
```

## 🎯 Logros del Proyecto

- ✅ Pipeline modular y mantenible
- ✅ Seguridad implementada en todas las capas
- ✅ CI/CD completo con 8 stages
- ✅ Arquitectura robusta con health checks
- ✅ Documentación exhaustiva con capturas
- ✅ Deploy automatizado
- ✅ HTTPS configurado

## 🔍 Testing

Tests automatizados en el pipeline:
- Health checks de todos los servicios
- Verificación de endpoints
- Tests de conectividad
- Validación de certificados SSL
