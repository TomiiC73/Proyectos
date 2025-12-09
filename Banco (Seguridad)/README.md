# 🏦 Banco Nacional - Sistema de Práctica de Vulnerabilidades

Sistema bancario web con vulnerabilidades intencionales para práctica ética de seguridad informática. Proyecto avanzado de la materia Seguridad de Sistemas que implementa múltiples vectores de ataque comunes en aplicaciones web.

## 📋 Descripción

Aplicación web bancaria desarrollada con Flask que simula un sistema bancario completo con **vulnerabilidades de seguridad implementadas intencionalmente** para el estudio y práctica de:
- Explotación ética de vulnerabilidades
- Técnicas de pentesting
- Análisis de seguridad en aplicaciones web
- Implementación correcta de OAuth2
- Mitigación de vulnerabilidades comunes

## 🎯 Vulnerabilidades Implementadas

### 1. Remote Code Execution (RCE) - CRÍTICO ⚠️
- **Ubicación:** `/transferencias`
- **Tipo:** Command Injection via `subprocess`
- **Descripción:** Permite ejecución arbitraria de comandos del sistema operativo
- **Riesgo:** Crítico - Control total del servidor
- **Desafío:** Incluye sistema de archivos simulado con pistas y exploits ocultos

### 2. OAuth2 Vulnerabilities - ALTO 🔓
- **State Parameter Missing (CSRF):** No valida el parámetro state en flujo OAuth
- **Client Secret Exposed:** Credenciales OAuth expuestas públicamente
- **JWT Weak Secret:** Secret débil para firma de tokens
- **Ubicación:** `/oauth/fakegoogle/*`
- **Riesgo:** Alto - Secuestro de cuentas y CSRF
- **Incluye:** Implementación completa de proveedor OAuth falso (FakeGoogle)

### 3. Otras Vulnerabilidades
- SQL Injection potencial
- Credenciales hardcodeadas
- Sesiones inseguras
- Secret keys expuestas

## 🏗️ Arquitectura

### Componentes Principales

```
├── app_banco.py              - Aplicación principal del banco
├── app_enunciados.py         - Sistema de enunciados y guías
├── templates/                - Vistas HTML del sistema bancario
│   ├── banco_*.html         - Páginas del banco
│   ├── oauth_*.html         - Sistema OAuth FakeGoogle
│   └── desafio_*.html       - Páginas de desafíos
├── docs/                    - Documentación completa
│   ├── README.md           - Guía principal
│   ├── OAUTH_VULNERABILITIES.md
│   └── DESAFIO_EXPLORACION.md
├── home/, etc/, opt/        - Sistema de archivos simulado
└── docker/                  - Configuración Docker
```

### Sistema de Archivos Simulado

El proyecto incluye una estructura de directorios realista con:
- `/home/admin/` - Archivos del administrador (contraseñas, SSH keys)
- `/opt/scripts/` - Scripts del sistema (con exploits ocultos)
- `/etc/config/` - Archivos de configuración
- `/var/log/` - Logs del sistema con pistas

## 🚀 Instalación y Ejecución

### 🐳 Opción 1: Docker (RECOMENDADO)

**Requisitos:** Docker y Docker Compose

```bash
# Windows
.\docker-build.bat
# Seleccionar opción 3: Construir e iniciar

# Linux/Mac
chmod +x docker-build.sh
./docker-build.sh
```

**URLs de acceso:**
- **Banco:** http://localhost:5000
- **Enunciados:** http://localhost:5001
- **Adminer (DB):** http://localhost:8080

### 🐧 Opción 2: WSL Ubuntu

```bash
.\run_wsl.bat
```

Permite ejecutar comandos Linux nativos en la vulnerabilidad RCE.

### 💻 Opción 3: Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicaciones
python app_banco.py          # Puerto 5000
python app_enunciados.py     # Puerto 5001
```

## 🔐 Credenciales de Acceso

### Cuentas Bancarias (Login Tradicional)

| Usuario | Password | Tipo de Cuenta | Saldo |
|---------|----------|----------------|-------|
| julian  | juli123  | Premium        | $28,750.75 |

### Cuentas FakeGoogle (OAuth2)

| Email | Password | Tipo |
|-------|----------|------|
| usuario@google.com | google123 | Usuario normal |
| admin@google.com | admin123 | Administrador |
| test@google.com | test123 | Testing |
| maria.lopez@google.com | maria123 | Usuario normal |

## 🎮 Desafíos Disponibles

### Desafío 1: Remote Code Execution
1. Explotar la vulnerabilidad RCE en `/transferencias`
2. Explorar el sistema de archivos simulado
3. Encontrar el archivo `rce_exploit.py` oculto en `/opt/scripts/.hidden/`
4. Ejecutar el exploit automatizado

**Documentación:** `docs/DESAFIO_EXPLORACION.md`

### Desafío 2: OAuth CSRF Attack
1. Comprender el flujo OAuth2 vulnerable
2. Explotar la falta de validación del parámetro state
3. Realizar un ataque CSRF para secuestrar cuentas
4. Ver el desafío avanzado de OAuth

**Documentación:** `docs/OAUTH_VULNERABILITIES.md`

## 🔧 Tecnologías

- **Backend:** Flask 3.1.2 (Python)
- **Autenticación:** OAuth2 (implementación personalizada)
- **JWT:** PyJWT 2.10.1
- **Base de Datos:** SQLite
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Containerización:** Docker, Docker Compose
- **Testing:** Requests 2.32.5

## 📚 Documentación Completa

- **[Guía Principal](./docs/README.md)** - Instalación y uso detallado
- **[Vulnerabilidades OAuth](./docs/OAUTH_VULNERABILITIES.md)** - Análisis completo de OAuth2
- **[Desafío de Exploración](./docs/DESAFIO_EXPLORACION.md)** - Guía del desafío RCE
- **Scripts de inicio** - `INICIAR.bat`, `INICIAR.sh`

## 📁 Funcionalidades del Sistema

### Módulos Bancarios
- 🔐 **Login/Registro** - Tradicional y OAuth2
- 📊 **Dashboard** - Vista de cuenta personal
- 💸 **Transferencias** - Sistema vulnerable a RCE
- 💳 **Tarjetas** - Gestión de tarjetas de crédito
- 📄 **Facturas** - Pago de servicios
- 💰 **Préstamos** - Solicitud de préstamos
- 📈 **Cotizaciones** - Información financiera
- 🏢 **Sucursales** - Ubicaciones
- 📞 **Contacto** - Formulario de contacto

### Sistema OAuth FakeGoogle
- Flujo de autorización completo
- Login con FakeGoogle
- Callback vulnerable (sin validación state)
- Generación de tokens JWT
- Información de usuario

### Sistema de Enunciados
- Aplicación separada con guías interactivas
- Desafíos de OAuth básico y avanzado
- Desafío de RCE con pistas
- Navegación por vulnerabilidades

## 🎯 Objetivos Académicos

Este proyecto fue desarrollado para la materia **Seguridad de Sistemas** con los objetivos de:

1. **Comprender vulnerabilidades reales** en aplicaciones web
2. **Practicar técnicas de pentesting** de forma ética
3. **Aprender implementación correcta** de OAuth2
4. **Identificar y explotar** Command Injection
5. **Desarrollar habilidades** de análisis de seguridad
6. **Entender la importancia** de la validación de entrada
7. **Practicar explotación** en entornos controlados

## 🛠️ Herramientas Incluidas

### Scripts de Explotación
- `tools/solucion_rce.py` - Exploit automatizado para RCE
- `opt/scripts/.hidden/rce_exploit.py` - Exploit oculto (desafío)

### Scripts del Sistema
- `scripts/docker-build.sh` - Construcción Docker
- `scripts/INICIAR.sh` - Inicio rápido
- `Makefile` - Automatización de tareas

### Archivos de Configuración
- `.env.example` - Variables de entorno
- `docker-compose.yml` - Orquestación de contenedores
- `requirements.txt` - Dependencias Python

## 🔍 Ejemplo de Explotación RCE

```bash
# 1. Login en el banco
Usuario: julian
Password: juli123

# 2. Ir a Transferencias

# 3. Inyectar comando en "Cuenta Destino"
; whoami

# 4. Explorar sistema
; ls -la /opt/scripts/
; find / -name "*exploit*" 2>/dev/null
; cat /opt/scripts/.hidden/rce_exploit.py
```

## 📊 Datos de Ejemplo

El sistema incluye 9 cuentas bancarias de ejemplo con:
- Diferentes tipos (Corriente, Ahorro, Premium)
- Saldos variables ($3,200 - $45,000)
- Cuentas con y sin credenciales de login

## 🎓 Reconocimientos

Proyecto desarrollado como Trabajo Práctico Integrador de **Seguridad de Sistemas**.
Implementa escenarios reales de vulnerabilidades para fomentar el aprendizaje práctico de seguridad informática.

---