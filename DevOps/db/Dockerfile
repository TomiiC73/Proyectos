# Imagen oficial de MySQL 9.4
FROM mysql:9.4

# Actualizar setuptools (corrección de CVE-2025-47273)
RUN microdnf install -y python3-pip && \
    pip install --no-cache-dir --upgrade pip setuptools==78.1.1 && \
    microdnf clean all

# Copiamos scripts de inicialización
COPY ./init-scripts/*.sql /docker-entrypoint-initdb.d/

# Puerto interno (solo entre contenedores)
EXPOSE 3306

HEALTHCHECK --interval=30s --timeout=20s --retries=10 \
    CMD mysqladmin ping -h localhost || exit 1

# Persistencia de datos
VOLUME ["/var/lib/mysql"]