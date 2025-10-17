# Multi-stage build para aplicación React
FROM node:18-alpine AS builder

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar todas las dependencias (incluyendo devDependencies para el build)
RUN npm install

# Copiar código fuente
COPY . .

# Build de la aplicación para producción
RUN npm run build

# Imagen final con nginx
FROM nginx:1.25-alpine

# Instalar curl para healthcheck
RUN apk add --no-cache curl

# Crear usuario no privilegiado
RUN addgroup -S nginxgroup && adduser -S nginxuser -G nginxgroup

# Copiar configuración personalizada de nginx
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copiar archivos build desde el stage anterior
COPY --from=builder /app/build /usr/share/nginx/html

# Configurar permisos correctos
RUN chown -R nginxuser:nginxgroup /usr/share/nginx/html && \
    chown -R nginxuser:nginxgroup /var/cache/nginx && \
    chown -R nginxuser:nginxgroup /var/log/nginx && \
    chown -R nginxuser:nginxgroup /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginxuser:nginxgroup /var/run/nginx.pid

# Exponer puerto
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Cambiar al usuario no privilegiado
USER nginxuser

# Comando de inicio
CMD ["nginx", "-g", "daemon off;"]
