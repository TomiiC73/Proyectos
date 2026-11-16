# Imagen oficial de MySQL 8.0 (versión estable LTS)
FROM mysql:8.4

# Copiamos scripts de inicialización
COPY ./init-scripts/*.sql /docker-entrypoint-initdb.d/

# Puerto interno (solo entre contenedores)
EXPOSE 3306

# Healthcheck básico para MySQL
HEALTHCHECK --interval=30s --timeout=10s --retries=5 CMD mysqladmin ping -h localhost || exit 1

# Persistencia de datos
VOLUME ["/var/lib/mysql"]

# Ejecutar como usuario mysql (no root)--------------------------
USER mysql