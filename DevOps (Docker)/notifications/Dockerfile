# Dockerfile para Microservicio de Notificaciones
# Imagen base optimizada para Python
FROM python:3.11-slim

# Variables de entorno para optimización
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV PORT=8001
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8001

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY simple_app.py ./
COPY .env ./

# Crear directorios necesarios
RUN mkdir -p /app/logs \
    && mkdir -p /app/temp \
    && chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Puerto que expone la aplicación
EXPOSE $PORT

# Healthcheck simplificado
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Comando para ejecutar la aplicación
CMD ["python", "simple_app.py"]
