# Portafolio de Proyectos

Colección de proyectos académicos desarrollados durante la carrera de Ingeniería en Sistemas de Información en la UTN FRC.

## 📁 Proyectos

### [Agencias](./Agencias)
Sistema de gestión de pruebas de vehículos para agencias automotrices. Implementa una API REST con Spring Boot y arquitectura de microservicios, incluyendo API Gateway y servicio de notificaciones. El proyecto incluye autenticación y autorización mediante OAuth2.

**Tecnologías:** Java, Spring Boot, Spring Cloud Gateway, MySQL, OAuth2

---

### [BonVino](./BonVino)
Aplicación web para gestión de ranking de vinos en bodegas. Implementa el patrón de diseño Iterator para búsqueda de vinos y reseñas de sommeliers. Sistema completo con frontend React y backend Spring Boot.

**Tecnologías:** Java, Spring Boot, React, JPA/Hibernate, MySQL

---

### [DevOps (Docker)](./DevOps%20(Docker))
Aplicación TODO dockerizada con arquitectura de microservicios. Implementa prácticas de seguridad con Docker Secrets, gestión de configuración y orquestación con Docker Compose. Incluye frontend React, backend Flask, servicio de notificaciones FastAPI y proxy reverso Nginx.

**Tecnologías:** Docker, Docker Compose, React, Flask, FastAPI, MySQL, Nginx

---

### [DevOps (Gitlab CI/CD)](./DevOps%20(Gitlab%20CI/CD))
Evolución del proyecto Docker con implementación completa de CI/CD en GitLab. Pipeline automatizado con 8 stages: escaneo de secretos, linting de código, análisis de Dockerfiles, escaneo de infraestructura, build, escaneo de vulnerabilidades, deploy y tests de producción. Implementa HTTPS y mejores prácticas de seguridad.

**Tecnologías:** GitLab CI/CD, Docker, Trivy, Checkov, detect-secrets, React, Flask, FastAPI, Nginx

---

### [Banco (Seguridad)](./Banco%20(Seguridad))
Sistema bancario web avanzado con múltiples vulnerabilidades intencionales para práctica ética de seguridad informática. Implementa Remote Code Execution (RCE), vulnerabilidades OAuth2 completas (CSRF, Client Secret expuesto), sistema de archivos simulado con exploits ocultos, y desafíos de pentesting. Incluye aplicación de enunciados, containerización con Docker y documentación exhaustiva.

**Tecnologías:** Python, Flask, OAuth2, JWT, Docker, SQLite, Bootstrap

---

## 🎓 Contexto Académico

Estos proyectos fueron desarrollados como trabajos prácticos de diferentes materias:
- **Backend de Aplicaciones** - Agencias
- **Diseño de Sistemas de Información** - BonVino  
- **Desarrollo y Operaciones (DevOps)** - Proyectos Docker y GitLab CI/CD
- **Seguridad de Sistemas** - Banco (Seguridad), TPI-SDS-main

## 🛠️ Tecnologías Principales

- **Backend:** Java (Spring Boot), Python (Flask, FastAPI)
- **Frontend:** React, Bootstrap 5
- **Bases de Datos:** MySQL, SQLite
- **DevOps:** Docker, Docker Compose, GitLab CI/CD, Nginx
- **Seguridad:** OAuth2, JWT, Docker Secrets, Trivy, Checkov
- **Testing:** JUnit, Postman, Requests

## 📝 Notas

Cada carpeta de proyecto contiene su propio README con instrucciones detalladas de configuración y ejecución.
