# Imagen base liviana de nginx
FROM nginx:1.29-alpine

# Instalar curl para healthcheck y gettext para envsubst
RUN apk add --no-cache curl gettext

# Copiar configuración como template y script de entrada
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Ejecutar como root (necesario para mkdir y chown en carpetas del sistema)
RUN mkdir -p /usr/share/nginx/html \
    /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    /var/run/nginx \
    # CHOWN: Asegurar que el usuario NGINX pueda escribir en sus carpetas de caché
    && chown -R nginx:nginx /var/cache/nginx \
    /var/log/nginx \
    /var/run/nginx \
    # CHMOD: Establecer permisos
    && chmod -R 755 /var/cache/nginx \
    /var/run/nginx \
    && chmod -R 644 /etc/nginx/nginx.conf \
    && rm -rf /var/cache/apk/*

# Debemos usar el usuario 'nginx' para el CMD
# ya que el proceso principal de Nginx está diseñado para correr con este usuario
# para funcionar correctamente y con permisos limitados
# USER nginx

# Exponer puerto
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Comando de inicio
CMD ["/entrypoint.sh"]