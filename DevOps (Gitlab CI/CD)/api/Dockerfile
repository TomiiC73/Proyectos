# Imagen base de Python optimizada
FROM python:3.11-alpine

# Variables de entorno para optimización
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requerimientos
COPY requirements.txt .

# Antes de cambiar al usuario no-root, instalar dependencias del sistema
# Usamos && para reducir las capas de la imagen, mientras mas RUNs haya,
# mas grande será la imagen final, ya que cuando instalamos los paquetes y no eliminar la caché residual en la misma sentencia, estos datos quedan en caché, por mas de que se los elimine después por medio de otro RUN, ya que no se eliminarán los de la capa anterior, quedando ocultos.
# permite también atomicidad, si una cosa falla, falla todo.
# Instalar dependencias del sistema necesarias
RUN apk update \
    && apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    mariadb-dev \
    python3-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && rm -rf /var/lib/apk/lists/*

# Crear usuario no-root para seguridad
# Este estará dentro de un grupo de usuario dedicado a servicios y apps ya que no se necesita de interacción humana mediante
# La segunda parte del comando agrega un usuario sin home ni shell al grupo que creamos antes
RUN addgroup -S appuser && adduser -S appuser -G appuser

# Copiar código de la aplicación
COPY --chown=appuser:appuser . .

# Cambiar al usuario no-root
USER appuser

# Exponer puerto
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')"

# Comando para ejecutar la aplicación
CMD ["python", "api.py"]
