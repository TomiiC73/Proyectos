#!/bin/sh

# Las variables de entorno ya están disponibles desde docker-compose
# Solo necesitamos procesar el template

# Procesar template de nginx con envsubst
envsubst '$NGINX_PORT $API_UPSTREAM $WEB_UPSTREAM $NOTIFICATIONS_UPSTREAM' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Verificar que la configuración es válida
nginx -t

# Iniciar nginx
exec nginx -g "daemon off;"