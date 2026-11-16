# Imagen base liviana de nginx
FROM nginx:1.29-alpine

# Instalar wget para healthcheck, gettext para envsubst y openssl para certificados
RUN apk add --no-cache wget gettext openssl

# Copiar configuración como template y script de entrada
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY entrypoint.sh /entrypoint.sh

# Convertir CRLF a LF y hacer ejecutable (corrige problemas de Windows)
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

# Crear directorios necesarios con permisos correctos
RUN mkdir -p /usr/share/nginx/html \
    /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    /var/run/nginx \
    /etc/nginx/ssl \
    /etc/nginx/templates \
    /etc/nginx/conf.d \
    && chown -R nginx:nginx /var/cache/nginx \
    /var/log/nginx \
    /var/run/nginx \
    /etc/nginx/ssl \
    /etc/nginx/templates \
    /etc/nginx/conf.d \
    && chmod -R 755 /var/cache/nginx \
    /var/run/nginx \
    /etc/nginx/ssl \
    && chmod 644 /etc/nginx/nginx.conf \
    && rm -rf /var/cache/apk/*

# Exponer puertos HTTP y HTTPS
EXPOSE 80 443

# Healthcheck usando endpoint /health que no redirige
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=60s \
    CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1

# Comando de inicio (como root para generar certificados SSL)
CMD ["/entrypoint.sh"]