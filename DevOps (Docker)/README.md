# DevOps - Aplicación TODO con Docker

Aplicación de gestión de tareas completamente dockerizada con arquitectura de microservicios. Proyecto enfocado en prácticas de seguridad, gestión de secretos y orquestación de contenedores.

## 📋 Descripción

Trabajo práctico de la materia DevOps que implementa una aplicación TODO con 5 microservicios containerizados. El proyecto hace énfasis en:
- Dockerización segura de aplicaciones
- Gestión de secretos con Docker Secrets
- Arquitectura de microservicios
- Configuración de proxy reverso

## 🏗️ Arquitectura

### Microservicios

| Servicio | Tecnología | Puerto | Descripción |
|----------|-----------|--------|-------------|
| **web** | React 18 + Nginx | 3000 | Frontend de la aplicación |
| **api** | Flask 3.1 | 5000 | API REST para gestión de tareas |
| **notifications** | FastAPI 0.118 | 8001 | Servicio de notificaciones por email |
| **db** | MySQL 9.4 | 3306 | Base de datos |
| **nginx** | Nginx 1.29 | 80 | Proxy reverso y balanceador |

## 🔧 Tecnologías

- **Orquestación:** Docker Compose
- **Frontend:** React, Nginx
- **Backend:** Flask (Python), FastAPI
- **Base de Datos:** MySQL
- **Proxy:** Nginx
- **Seguridad:** Docker Secrets

## 🚀 Inicio Rápido

```bash
# Levantar todos los servicios
./deploy.sh

# Acceder a la aplicación
http://localhost
```

La aplicación estará disponible en:
- Frontend: `http://localhost`
- API: `http://localhost/api`
- Notificaciones: `http://localhost/notifications`

## 🔐 Seguridad

El proyecto implementa **Docker Secrets** para la gestión segura de credenciales:
- Contraseñas de base de datos
- Claves secretas de Flask
- Credenciales SMTP para notificaciones

Ver documentación detallada en [`READMES/SECRETS.md`](./READMES/SECRETS.md)

## 📚 Documentación Adicional

- **[README Principal](./READMES/README.md)**: Guía completa del proyecto
- **[Gestión de Errores](./READMES/ERRORES.md)**: Problemas comunes y soluciones
- **[Seguridad](./READMES/SEGURIDAD.md)**: Implementación de seguridad
- **[Secretos](./READMES/SECRETS.md)**: Guía de Docker Secrets

## 📁 Estructura

```
api/              - Servicio Flask (Backend API)
web/              - Servicio React (Frontend)
notifications/    - Servicio FastAPI (Notificaciones)
db/               - Configuración MySQL
nginx/            - Configuración proxy reverso
READMES/          - Documentación completa
```

## 🎯 Objetivo Académico

Aplicar conocimientos de DevOps para:
- Containerizar aplicaciones
- Implementar arquitecturas de microservicios
- Gestionar secretos de forma segura
- Configurar proxy reverso y networking
- Trabajar en equipo con documentación clara
