# Gestión de Secretos - Sistema Seguro

[![Docker](https://img.shields.io/badge/Docker-Secrets-blue?logo=docker)](https://docs.docker.com/engine/swarm/secrets/)
[![Security](https://img.shields.io/badge/Security-Enabled-green?logo=shield)](https://security.com/)

Este proyecto utiliza **Docker Secrets** y un sistema seguro de gestión de credenciales que **NO sube secretos al repositorio Git**. Compatible con MySQL 9.4, Flask 3.0, FastAPI 0.115 y toda la arquitectura dockerizada.

## Estructura de Secretos

```
secrets/
├── .gitkeep                        # Mantiene la estructura en Git
├── db_password.txt                 # Contraseña del usuario de BD (NO en Git)
├── db_root_password.txt            # Contraseña root de MySQL (NO en Git)
├── flask_secret_key.txt            # Secret key para Flask (NO en Git)
├── smtp_username.txt               # Email de Gmail (NO en Git)
├── smtp_password.txt               # App Password de Gmail (NO en Git)
├── db_password.txt.example         # Ejemplo para BD
├── db_root_password.txt.example    # Ejemplo para root
├── flask_secret_key.txt.example    # Ejemplo para Flask secret
├── smtp_username.txt.example       # Ejemplo para email
└── smtp_password.txt.example       # Ejemplo para password
```

## Configuración Inicial

### 1. Ejecutar el Script de Despliegue
```bash
bash deploy.sh
```
El script creará automáticamente los archivos de secretos con valores por defecto.

### 2. Configurar Credenciales Reales

#### Para Email (Gmail):
1. Ve a: https://myaccount.google.com/apppasswords
2. Genera un App Password de 16 dígitos
3. Edita los archivos:
   ```bash
   echo "tu-email@gmail.com" > secrets/smtp_username.txt
   echo "abcd-efgh-ijkl-mnop" > secrets/smtp_password.txt  # Tu App Password real
   ```

#### Para Base de Datos:
```bash
echo "MiPasswordSuperSeguro123!" > secrets/db_password.txt
echo "RootPasswordUltraSeguro456!" > secrets/db_root_password.txt
```

#### Para Flask Secret Key:
```bash
# Generar una clave aleatoria segura
python -c "import secrets; print(secrets.token_hex(32))" > secrets/flask_secret_key.txt
# O usar una clave personalizada
echo "tu-clave-secreta-super-segura-de-64-caracteres-minimo" > secrets/flask_secret_key.txt
```

## Seguridad

### Lo que SÍ se sube a Git:
- Archivos `.example` con plantillas
- Estructura de directorios
- Documentación
- Código fuente

### Lo que NO se sube a Git:
- Archivos `.env` con datos reales
- Archivos `secrets/*.txt` con credenciales
- Contraseñas o tokens reales
- Credenciales de servicios externos

## Docker Secrets

El proyecto usa [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/) para cargar credenciales de forma segura:

```yaml
# En docker-compose.yml
environment:
  SMTP_USERNAME_FILE: /run/secrets/smtp_username  # Archivo, no variable directa
  SMTP_PASSWORD_FILE: /run/secrets/smtp_password

secrets:
  smtp_username:
    file: ./secrets/smtp_username.txt  # Archivo local se monta como secreto
  smtp_password:
    file: ./secrets/smtp_password.txt
```

## Desarrollo Local vs Producción

### Desarrollo Local:
- Archivos de secretos en `./secrets/`
- Variables no sensibles en docker-compose
- Simulación de email si no hay credenciales reales

### Producción:
- Usar servicios de secretos (AWS Secrets Manager, Azure Key Vault, etc.)
- Variables de entorno desde CI/CD
- Rotación automática de credenciales

## Solución de Problemas

### Email no se envía:
1. Verifica que `secrets/smtp_username.txt` tenga tu email real
2. Verifica que `secrets/smtp_password.txt` tenga tu App Password de Gmail
3. Revisa los logs: `docker-compose logs notifications`

### Base de datos no conecta:
1. Verifica que `secrets/db_password.txt` tenga la contraseña correcta
2. Verifica que coincida con `secrets/db_root_password.txt`
3. Revisa los logs: `docker-compose logs db`

## Recursos

- [Crear App Password de Gmail](https://support.google.com/accounts/answer/185833)
- [Docker Secrets Documentation](https://docs.docker.com/engine/swarm/secrets/)
- [Security Best Practices](https://docs.docker.com/develop/security-best-practices/)