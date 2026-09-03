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

### [DevOps (Gitlab CI/CD)](./DevOps%20(Gitlab%20CI))
Evolución del proyecto Docker con implementación completa de CI/CD en GitLab. Pipeline automatizado con 8 stages: escaneo de secretos, linting de código, análisis de Dockerfiles, escaneo de infraestructura, build, escaneo de vulnerabilidades, deploy y tests de producción. Implementa HTTPS y mejores prácticas de seguridad.

**Tecnologías:** GitLab CI/CD, Docker, Trivy, Checkov, detect-secrets, React, Flask, FastAPI, Nginx

---

### [Banco (Seguridad)](./Banco%20(Seguridad))
Sistema bancario web avanzado con múltiples vulnerabilidades intencionales para práctica ética de seguridad informática. Implementa Remote Code Execution (RCE), vulnerabilidades OAuth2 completas (CSRF, Client Secret expuesto), sistema de archivos simulado con exploits ocultos, y desafíos de pentesting. Incluye aplicación de enunciados, containerización con Docker y documentación exhaustiva.

**Tecnologías:** Python, Flask, OAuth2, JWT, Docker, SQLite, Bootstrap

---

### [Aeropuertos — Cierre de Rampa (n8n)](./Proyectos%20n8n/aeropuertos-cierre-rampa-n8n)
Flujo de automatización en n8n que orquesta la respuesta operativa ante condiciones meteorológicas severas en rampa: evalúa un reporte METAR, identifica los vuelos en ventana de riesgo y dispara en paralelo las notificaciones a las áreas involucradas (pista, mantenimiento, terminal, auditoría). Demo técnica desarrollada para la defensa de un TPI.

**Tecnologías:** n8n, JavaScript, JSON (mock de datos meteorológicos y vuelos)

---

### [Trivia por Telegram (n8n)](./Proyectos%20n8n/trivia-telegram-n8n)
Bot de trivia en vivo (5 preguntas de opción múltiple, temática tech/n8n) construido sobre n8n Cloud con dos bots de Telegram: uno para jugadores y otro de administración para controlar la partida y ver respuestas en tiempo real. Al finalizar, envía automáticamente una tabla de clasificación a todos los participantes.

**Tecnologías:** n8n Cloud, Telegram Bot API, JavaScript

---

### [EscapeRoomHackerTech](./EscapeRoomHackerTech%20-%20UTNFRC)
Primera versión de "HackerBank", un banco ficticio usado como escape room de ciberseguridad para el evento HackerTech (UTN-FRC). El segundo factor de autenticación es reconocimiento facial sin detección de vida (liveness), pensado para que los participantes lo vulneren mostrando una foto a la cámara.

**Tecnologías:** Python, Flask, SQLite, Docker, reconocimiento facial

---

### [HackerTech](./HackerTech%20-%20UTNFRC)
Evolución de HackerBank para el evento HackerTech (UTN-FRC): reemplaza el reconocimiento facial por un segundo factor real con passkeys FIDO2/WebAuthn (Windows Hello, Touch ID), manteniendo el código del laboratorio anterior en `_legacy_face_auth/` como referencia. Incluye guía para el equipo instructor y un proxy de despliegue en Vercel.

**Tecnologías:** Python, Flask, WebAuthn/FIDO2, Docker, Vercel

---

### [Charla — Prompt Injection](./Charla)
Laboratorio demostrativo de un simulador de filtros ATS (Applicant Tracking System) con IA (Groq) sobre CVs en PDF, usado en una charla sobre prompt injection: incluye CVs de ejemplo con prompts ocultos para mostrar en vivo cómo un CV puede manipular la respuesta del modelo que lo evalúa.

**Tecnologías:** Node.js, Express, Groq SDK (LLM), pdf-parse, IMAP/SMTP

---

## 🎓 Contexto Académico

Estos proyectos fueron desarrollados como trabajos prácticos de diferentes materias:
- **Backend de Aplicaciones** - Agencias
- **Diseño de Sistemas de Información** - BonVino  
- **Desarrollo y Operaciones (DevOps)** - Proyectos Docker y GitLab CI/CD
- **Seguridad de Sistemas** - Banco (Seguridad), TPI-SDS-main

Los siguientes proyectos no son trabajos de cursada, sino desarrollos propios y material para eventos de extensión:
- **Automatización (n8n)** - Aeropuertos (Cierre de Rampa), Trivia por Telegram
- **HackerTech (UTN-FRC)** - EscapeRoomHackerTech, HackerTech
- **IA / Seguridad de IA** - Charla (Prompt Injection)

## 🛠️ Tecnologías Principales

- **Backend:** Java (Spring Boot), Python (Flask, FastAPI), Node.js (Express)
- **Frontend:** React, Bootstrap 5
- **Bases de Datos:** MySQL, SQLite
- **DevOps:** Docker, Docker Compose, GitLab CI/CD, Nginx, Vercel
- **Seguridad:** OAuth2, JWT, WebAuthn/FIDO2, Docker Secrets, Trivy, Checkov
- **Automatización / IA:** n8n, Telegram Bot API, Groq SDK (LLM)
- **Testing:** JUnit, Postman, Requests

## 📝 Notas

Cada carpeta de proyecto contiene su propio README con instrucciones detalladas de configuración y ejecución.
