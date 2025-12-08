# Bitácora del Pipeline CI/CD

## Pipeline Completo Exitoso

![Pipeline completo](imgs/pipeline-complete.png)

## Stages del Pipeline

### 1. Secrets Scan
Escaneo de secretos en el código fuente usando detect-secrets.

![Secrets Scan Stage](imgs/secrets-scan-jobs/1.%20secrets-scan.png)

#### Jobs individuales:
- **secrets:scan:api**: ![API](imgs/secrets-scan-jobs/secrets-scan-api.png)
- **secrets:scan:web**: ![Web](imgs/secrets-scan-jobs/secrets-scan-web.png)
- **secrets:scan:nginx**: ![Nginx](imgs/secrets-scan-jobs/secrets-scan-ngnix.png)
- **secrets:scan:notifications**: ![Notifications](imgs/secrets-scan-jobs/secrets-scan-notifications.png)

**Artefactos generados**:
![Artefactos Secrets Scan](imgs/secrets-scan-jobs/artifacts-secrets-scan.png)

---

### 2. Code Lint
Linting de código para Python (flake8, pylint) y JavaScript/TypeScript (eslint).

![Code Lint Stage](imgs/code-lint-jobs/2.%20code-lint.png)

#### Jobs individuales:
- **lint:python:api**: ![API Python](imgs/code-lint-jobs/code-lint-api.png)
- **lint:python:notifications**: ![Notifications Python](imgs/code-lint-jobs/code-lint-notifications.png)
- **lint:js:web**: ![Web JavaScript](imgs/code-lint-jobs/code-lint-web.png)

**Artefactos generados**:
![Artefactos Code Lint](imgs/code-lint-jobs/artifacts-code-lint.png)

---

### 3. Docker Lint
Análisis estático de Dockerfiles usando hadolint.

![Docker Lint Stage](imgs/docker-lint-jobs/3.%20docker-lint.png)

#### Jobs individuales:
- **docker-lint:api**: ![API Dockerfile](imgs/docker-lint-jobs/docker-lint-api.png)
- **docker-lint:web**: ![Web Dockerfile](imgs/docker-lint-jobs/docker-lint-web.png)
- **docker-lint:db**: ![DB Dockerfile](imgs/docker-lint-jobs/docker-lint-db.png)
- **docker-lint:nginx**: ![Nginx Dockerfile](imgs/docker-lint-jobs/docker-lint-nginx.png)
- **docker-lint:notifications**: ![Notifications Dockerfile](imgs/docker-lint-jobs/docker-lint-notifications.png)

**Artefactos generados**:
![Artefactos Docker Lint](imgs/docker-lint-jobs/artifacts-docker-lint.png)

---

### 4. IaC Scan
Escaneo de infraestructura como código usando Checkov.

![IaC Scan Stage](imgs/iac-scan-jobs/4.%20iac-scan.png)

#### Jobs individuales:
- **iac:scan:compose**: ![Docker Compose](imgs/iac-scan-jobs/iac-scan-compose.png)
- **iac:scan:dockerfiles**: ![Dockerfiles](imgs/iac-scan-jobs/iac-scan-dockerfiles.png)

**Artefactos generados**:
![Artefactos IaC Scan](imgs/iac-scan-jobs/artifacts-iac-scan.png)

---

### 5. Build
Construcción de imágenes Docker y push al registry del LabSis.

![Build Stage](imgs/build-jobs/5.%20build.png)

#### Jobs individuales:
- **build:api**: ![API Build](imgs/build-jobs/build-api.png)
- **build:web**: ![Web Build](imgs/build-jobs/build-web.png)
- **build:db**: ![DB Build](imgs/build-jobs/build-db.png)
- **build:nginx**: ![Nginx Build](imgs/build-jobs/build-ngnix.png)
- **build:notifications**: ![Notifications Build](imgs/build-jobs/build-notifications.png)

**Artefactos generados**:
![Artefactos Build](imgs/build-jobs/artifacts-build.png)

---

### 6. Image Scan
Escaneo de vulnerabilidades en imágenes Docker usando Trivy.

![Image Scan Stage](imgs/image-scan-jobs/6.%20image-scan.png)

#### Jobs individuales:
- **image:scan:api**: ![API Scan](imgs/image-scan-jobs/image-scan-api.png)
- **image:scan:web**: ![Web Scan](imgs/image-scan-jobs/image-scan-web.png)
- **image:scan:db**: ![DB Scan](imgs/image-scan-jobs/image-scan-db.png)
- **image:scan:nginx**: ![Nginx Scan](imgs/image-scan-jobs/image-scan-nginx.png)
- **image:scan:notifications**: ![Notifications Scan](imgs/image-scan-jobs/image-scan-notifications.png)

**Artefactos generados**:
![Artefactos Image Scan 1](imgs/image-scan-jobs/artifacts-image-scan-1.png)
![Artefactos Image Scan 2](imgs/image-scan-jobs/artifacts-image-scan-2.png)

---

### 7. Deploy
Despliegue en servidor mediante SSH.

![Deploy Stage](imgs/deploy-jobs/7.%20deploy.png)

#### Jobs individuales:
- **deploy:production**: ![Deploy Production](imgs/deploy-jobs/deploy-production.png)
- **deployment:deployment**: ![Deployment Process](imgs/deploy-jobs/deploy-deployment.png)

**Artefactos generados**:
![Artefactos Deploy](imgs/deploy-jobs/artifacts-deploy.png)

---

### 8. Production Tests
Tests de health checks en producción.

![Production Tests Stage](imgs/production-test-jobs/8.%20production-tests.png)

#### Jobs individuales:
- **production:health-checks**: ![Health Checks](imgs/production-test-jobs/production-tests-health-checks.png)

---

## Artefactos Generados

Cada job genera artefactos que se pueden descargar desde GitLab:

- **Secrets Scan**: Lista de secretos detectados (JSON)
- **Code Lint**: Reportes de flake8, pylint y ESLint (JSON)
- **Docker Lint**: Reportes de hadolint (JSON)
- **IaC Scan**: Reportes de Checkov (JSON)
- **Image Scan**: Reportes de Trivy (JSON + HTML con template personalizado)
- **Production Tests**: Respuestas de endpoints testeados (JSON)

## Variables de Entorno Configuradas

Las siguientes variables están configuradas en GitLab CI/CD:

- `CI_REGISTRY_USER`: Usuario del registry del LabSis
- `CI_REGISTRY_PASSWORD`: Contraseña del registry
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_ROOT_PASSWORD`: Contraseña root de MySQL
- `FLASK_SECRET_KEY`: Secret key para Flask
- `SMTP_USERNAME`: Usuario de SMTP
- `SMTP_PASSWORD`: Contraseña de SMTP

Todas marcadas como **Protected** y **Masked**.
