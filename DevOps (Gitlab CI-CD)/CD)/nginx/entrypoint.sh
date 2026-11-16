#!/bin/sh
set -e

echo "=========================================="
echo "🚀 NGINX STARTUP - Detailed Logs"
echo "=========================================="
echo "Timestamp: $(date)"
echo ""

# Generar certificados SSL self-signed si no existen
SSL_DIR="/etc/nginx/ssl"
echo "📁 Creando directorio SSL: $SSL_DIR"
mkdir -p "$SSL_DIR"
ls -lah "$SSL_DIR" || true

echo ""
echo "🔐 Verificando certificados SSL..."
if [ ! -f "$SSL_DIR/nginx-selfsigned.crt" ] || [ ! -f "$SSL_DIR/nginx-selfsigned.key" ]; then
    echo "⚠️  Certificados no encontrados - Generando nuevos..."
    echo "   Ejecutando: openssl req -x509 -nodes -days 365 -newkey rsa:2048"
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$SSL_DIR/nginx-selfsigned.key" \
        -out "$SSL_DIR/nginx-selfsigned.crt" \
        -subj "/C=AR/ST=Cordoba/L=Cordoba/O=UTN/OU=DevOps/CN=localhost"
    echo "✅ Certificados SSL generados exitosamente"
    ls -lh "$SSL_DIR/nginx-selfsigned"*
else
    echo "✅ Certificados SSL ya existen:"
    ls -lh "$SSL_DIR/nginx-selfsigned"*
fi

echo ""
echo "🔑 Verificando DH params..."
if [ ! -f "$SSL_DIR/dhparam.pem" ]; then
    echo "⚠️  DH params no encontrados - Generando (2048 bits)..."
    echo "   Esto tomará ~2-3 minutos..."
    START_TIME=$(date +%s)
    openssl dhparam -out "$SSL_DIR/dhparam.pem" 2048
    END_TIME=$(date +%s)
    ELAPSED=$((END_TIME - START_TIME))
    echo "✅ DH params generados en ${ELAPSED}s"
    ls -lh "$SSL_DIR/dhparam.pem"
else
    echo "✅ DH params ya existen:"
    ls -lh "$SSL_DIR/dhparam.pem"
fi

echo ""
echo "📋 Variables de entorno disponibles:"
echo "   WEB_UPSTREAM=${WEB_UPSTREAM:-NOT SET}"
echo "   API_UPSTREAM=${API_UPSTREAM:-NOT SET}"
echo "   NOTIFICATIONS_UPSTREAM=${NOTIFICATIONS_UPSTREAM:-NOT SET}"

echo ""
echo "⚙️  Procesando template de configuración nginx..."
echo "   Input:  /etc/nginx/templates/default.conf.template"
echo "   Output: /etc/nginx/conf.d/default.conf"
envsubst '${WEB_UPSTREAM} ${API_UPSTREAM} ${NOTIFICATIONS_UPSTREAM}' \
    < /etc/nginx/templates/default.conf.template \
    > /etc/nginx/conf.d/default.conf

if [ -f /etc/nginx/conf.d/default.conf ]; then
    echo "✅ Configuración procesada exitosamente"
    echo "   Tamaño: $(wc -c < /etc/nginx/conf.d/default.conf) bytes"
else
    echo "❌ ERROR: No se generó el archivo de configuración"
    exit 1
fi

echo ""
echo "🔍 Validando sintaxis de configuración nginx..."
if nginx -t 2>&1; then
    echo "✅ Configuración válida"
else
    echo "❌ ERROR: Configuración inválida"
    echo "Contenido de /etc/nginx/conf.d/default.conf:"
    cat /etc/nginx/conf.d/default.conf
    exit 1
fi

echo ""
echo "🌐 Verificando puertos y permisos..."
netstat -tuln 2>/dev/null || echo "   netstat no disponible"
id

echo ""
echo "=========================================="
echo "✅ INICIANDO NGINX"
echo "=========================================="
exec nginx -g "daemon off;"
