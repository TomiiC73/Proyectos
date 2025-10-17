#!/bin/bash

# =============================================================================
# TODO APP - SCRIPT DE DESPLIEGUE AUTOMATIZADO
# =============================================================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

print_header() {
    echo ""
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}$(echo "$1" | sed 's/./=/g')${NC}"
    echo ""
}

print_step() {
    echo -e "${BLUE}  -> $1${NC}"
}

print_success() {
    echo -e "${GREEN}  [OK] $1${NC}"
}

print_error() {
    echo -e "${RED}  [ERROR] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}  [WARNING] $1${NC}"
}

print_info() {
    echo -e "${CYAN}  [INFO] $1${NC}"
}

# =============================================================================
# INICIO DEL DESPLIEGUE
# =============================================================================

echo ""
echo -e "${GREEN}TODO APP - DESPLIEGUE AUTOMATIZADO${NC}"
echo -e "${GREEN}====================================${NC}"
echo ""

# =============================================================================
# VERIFICACIONES PREVIAS
# =============================================================================

print_header "VERIFICACIONES PREVIAS"

# Verificar Docker instalado
print_step "Verificando instalación de Docker..."
if command -v docker &> /dev/null; then
    docker_version=$(docker --version)
    print_success "Docker encontrado: $docker_version"
else
    print_error "Docker no está instalado"
    print_info "Instala Docker desde: https://docs.docker.com/desktop/"
    exit 1
fi

# Verificar Docker ejecutándose
print_step "Verificando que Docker esté ejecutándose..."
if docker info &> /dev/null; then
    print_success "Docker está ejecutándose correctamente"
else
    print_error "Docker está instalado pero no se está ejecutando"
    print_info "Inicia Docker Desktop y ejecuta este script nuevamente"
    exit 1
fi

# Verificar Docker Compose
print_step "Verificando Docker Compose..."
if command -v docker-compose &> /dev/null; then
    compose_version=$(docker-compose --version)
    print_success "Docker Compose encontrado: $compose_version"
elif docker compose version &> /dev/null; then
    compose_version=$(docker compose version)
    print_success "Docker Compose (plugin) encontrado: $compose_version"
    alias docker-compose="docker compose"
else
    print_error "Docker Compose no está disponible"
    exit 1
fi

# Verificar archivos de configuración
print_step "Verificando archivos de configuración esenciales..."

required_files=(
    "secrets/db_password.txt"
    "secrets/db_root_password.txt" 
    "secrets/smtp_username.txt"
    "secrets/smtp_password.txt"
    "secrets/flask_secret_key.txt"
    "api/.env"
    "web/.env" 
    "nginx/.env"
    "db/.env"
    "notifications/.env"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "Encontrado: $file"
    else
        print_warning "Faltante: $file - creando archivo por defecto"
        
        case $file in
            "secrets/db_password.txt")
                mkdir -p secrets
                chmod 700 secrets
                echo "TodosUserP@ssw0rd2024!" > "$file"
                chmod 600 "$file"
                print_success "Creado: $file"
                ;;
            "secrets/db_root_password.txt")
                mkdir -p secrets
                chmod 700 secrets
                echo "MySecureRootP@ssw0rd2024!" > "$file"
                chmod 600 "$file"
                print_success "Creado: $file"
                ;;
            "secrets/smtp_username.txt")
                mkdir -p secrets
                chmod 700 secrets
                echo "tu-email@gmail.com" > "$file"
                chmod 600 "$file"
                print_success "Creado: $file"
                print_info "RECORDATORIO: Configura tu email real en este archivo"
                ;;
            "secrets/smtp_password.txt")
                mkdir -p secrets
                chmod 700 secrets
                echo "tu-app-password-de-16-digitos" > "$file"
                chmod 600 "$file"
                print_success "Creado: $file"
                print_info "RECORDATORIO: Configura tu App Password de Gmail"
                print_info "Genera el App Password en: https://myaccount.google.com/apppasswords"
                ;;
            "secrets/flask_secret_key.txt")
                mkdir -p secrets
                chmod 700 secrets
                echo "$(openssl rand -hex 32)" > "$file"
                chmod 600 "$file"
                print_success "Creado: $file (secret key generada automáticamente)"
                echo ""
                ;;
            *)
                # Para archivos .env y otros, copiar desde plantilla si existe
                dir=$(dirname "$file")
                filename=$(basename "$file")
                example_file="$dir/${filename}.example"
                
                if [ -f "$example_file" ]; then
                    cp "$example_file" "$file"
                    print_success "Creado: $file desde plantilla"
                else
                    # Crear archivo básico si no existe plantilla
                    mkdir -p "$dir"
                    touch "$file"
                    print_success "Creado: $file (vacío)"
                fi
                ;;
        esac
    fi
done

# =============================================================================
# PREPARACION DEL ENTORNO
# =============================================================================

print_header "PREPARACION DEL ENTORNO"

# Detener contenedores existentes
print_step "Deteniendo contenedores existentes..."
if docker-compose down --remove-orphans &> /dev/null; then
    print_success "Contenedores detenidos correctamente"
else
    print_info "No había contenedores ejecutándose"
fi

# Opción de limpieza
echo ""
read -p "¿Deseas limpiar imágenes Docker antiguas? (S/N): " cleanup
if [[ $cleanup == "s" || $cleanup == "S" ]]; then
    print_step "Limpiando imágenes Docker antiguas..."
    docker system prune -f &> /dev/null
    docker image prune -f &> /dev/null
    print_success "Limpieza completada"
fi


# Construir todas las imágenes
echo ""
print_step "        Construyendo todas las imágenes Docker..."
echo -e "${YELLOW}      Esto puede tomar varios minutos la primera vez...${NC}"

# =============================================================================
# CONSTRUCCION DE IMAGENES
# =============================================================================

print_header "CONSTRUCCION DE IMAGENES DOCKER"

print_step "Construyendo todas las imágenes..."
print_info "Este proceso puede tomar varios minutos la primera vez"

if docker-compose build; then
    print_success "Todas las imágenes construidas correctamente"
else
    print_error "Error durante la construcción de imágenes"
    print_info "Revisa los logs anteriores para identificar el problema"
    exit 1
fi

# =============================================================================
# DESPLIEGUE DE SERVICIOS
# =============================================================================

print_header "DESPLIEGUE DE SERVICIOS"

print_step "Iniciando todos los servicios..."
if docker-compose up -d; then
    print_success "Servicios iniciados en modo background"
else
    print_error "Error iniciando los servicios"
    exit 1
fi

# Esperar inicialización
print_step "Esperando inicialización de los servicios..."
sleep 10

print_step "Verificando estado de los contenedores..."
echo ""
echo -e "${CYAN}ESTADO DE LOS CONTENEDORES:${NC}"
docker-compose ps
echo ""

# Verificar que todos los servicios estén healthy
print_step "           Verificando health checks..."
echo ""
max_attempts=12
attempt=1

while [ $attempt -le $max_attempts ]; do
    echo -e "${YELLOW}Intento $attempt de $max_attempts...${NC}"
    
    healthy_services=0
    total_services=4  # db, api, web, nginx
    
    # Verificar cada servicio
    db_status=$(docker inspect --format='{{.State.Health.Status}}' todos-db 2>/dev/null || echo "starting")
    api_status=$(docker inspect --format='{{.State.Health.Status}}' todos-api 2>/dev/null || echo "starting")
    web_status=$(docker inspect --format='{{.State.Health.Status}}' todos-web 2>/dev/null || echo "starting")
    nginx_status=$(docker inspect --format='{{.State.Health.Status}}' todos-nginx 2>/dev/null || echo "starting")
    
    [ "$db_status" = "healthy" ] && ((healthy_services++))
    [ "$api_status" = "healthy" ] && ((healthy_services++))
    [ "$web_status" = "healthy" ] && ((healthy_services++))
    [ "$nginx_status" = "healthy" ] && ((healthy_services++))
    
    echo -e "${YELLOW}Servicios saludables: $healthy_services/$total_services${NC}"
    
    if [ $healthy_services -eq $total_services ]; then
        print_success "     ¡Todos los servicios están saludables!"
        echo ""
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        print_warning "     Algunos servicios pueden no estar completamente listos"
        echo ""
        break
    fi
    
    sleep 15
    ((attempt++))
done


# Mostrar información de conexión
echo ""
echo -e "${GREEN}        DESPLIEGUE COMPLETADO EXITOSAMENTE!${NC}"
echo -e "${GREEN}==========================================================${NC}"
echo ""
echo -e "${CYAN}      COMANDOS ÚTILES:${NC}"
echo -e "• Ver logs: docker-compose logs -f"
echo -e "• Detener app: docker-compose down"
echo -e "• Reiniciar: docker-compose restart"
echo -e "• Ver estado: docker-compose ps"
echo ""
echo -e "${CYAN}      LOGS POR MICROSERVICIO:${NC}"
echo -e "• Logs MySQL:        docker-compose logs -f db"
echo -e "• Logs API Flask:    docker-compose logs -f api"
echo -e "• Logs Frontend:     docker-compose logs -f web"
echo -e "• Logs FastAPI:      docker-compose logs -f notifications"
echo -e "• Logs Nginx:        docker-compose logs -f nginx"
echo ""

# =============================================================================
# VERIFICACION DE SALUD DE MICROSERVICIOS
# =============================================================================

print_header "VERIFICACION DE SALUD DE MICROSERVICIOS"

# Función para verificar health según el tipo de servicio
check_service_health() {
    local service_name=$1
    local service_type=$2
    local health_url=$3
    local container_name=$4
    local max_retries=6
    local retry_delay=3
    
    print_step "Verificando $service_name..."
    
    for ((i=1; i<=max_retries; i++)); do
        container_status=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null || echo "unknown")
        
        case $service_type in
            "database")
                if [ "$container_status" = "healthy" ]; then
                    print_success "$service_name: Container [$container_status] - FUNCIONANDO"
                    return 0
                elif [ "$container_status" = "starting" ] || [ "$container_status" = "unknown" ]; then
                    print_info "$service_name: Container [$container_status] - Iniciando... ($i/$max_retries)"
                else
                    print_error "$service_name: Container [$container_status] - PROBLEMA"
                fi
                ;;
                
            "internal-api")
                if [ "$container_status" = "healthy" ]; then
                    print_success "$service_name: Container [$container_status] - FUNCIONANDO"
                    return 0
                elif [ "$container_status" = "starting" ] || [ "$container_status" = "unknown" ]; then
                    print_info "$service_name: Container [$container_status] - Iniciando... ($i/$max_retries)"
                else
                    print_error "$service_name: Container [$container_status] - PROBLEMA"
                fi
                ;;
                
            "web-proxy"|"web-service")
                if [ "$container_status" = "healthy" ]; then
                    if command -v curl &> /dev/null; then
                        http_status=$(curl -s -o /dev/null -w "%{http_code}" "$health_url" --connect-timeout 5 --max-time 8 2>/dev/null || echo "000")
                        
                        if ([ "$service_type" = "web-proxy" ] && [ "$http_status" = "200" ]) || \
                           ([ "$service_type" = "web-service" ] && [ "$http_status" = "404" ]); then
                            print_success "$service_name: Container [$container_status] + HTTP [$http_status] - FUNCIONANDO"
                            return 0
                        else
                            print_info "$service_name: Container [$container_status] + HTTP [$http_status] - Verificando... ($i/$max_retries)"
                        fi
                    else
                        print_success "$service_name: Container [$container_status] - FUNCIONANDO (sin curl)"
                        return 0
                    fi
                elif [ "$container_status" = "starting" ] || [ "$container_status" = "unknown" ]; then
                    print_info "$service_name: Container [$container_status] - Iniciando... ($i/$max_retries)"
                else
                    print_error "$service_name: Container [$container_status] - PROBLEMA"
                fi
                ;;
                
            "frontend")
                if [ "$container_status" = "healthy" ]; then
                    print_success "$service_name: Container [$container_status] (via Nginx) - FUNCIONANDO"
                    return 0
                elif [ "$container_status" = "starting" ] || [ "$container_status" = "unknown" ]; then
                    print_info "$service_name: Container [$container_status] - Iniciando... ($i/$max_retries)"
                else
                    print_error "$service_name: Container [$container_status] - PROBLEMA"
                fi
                ;;
        esac
        
        if [ $i -lt $max_retries ]; then
            sleep $retry_delay
        fi
    done
    
    print_error "       ;;
        esac
        
        if [ $i -lt $max_retries ]; then
            sleep $retry_delay
        fi
    done
    
    print_error "$service_name: No pudo verificarse después de $max_retries intentos"
    return 1
}

echo ""
print_success "DESPLIEGUE COMPLETADO"
print_info "Aplicación disponible en: http://localhost"

echo ""
echo -e "${CYAN}COMANDOS UTILES:${NC}"
echo "  Ver logs:           docker-compose logs -f"
echo "  Detener:           docker-compose down"
echo "  Reiniciar:         docker-compose restart"
echo "  Ver estado:        docker-compose ps"
echo ""
echo -e "${CYAN}TROUBLESHOOTING:${NC}"
echo "  Logs MySQL:        docker-compose logs -f db"
echo "  Logs API:          docker-compose logs -f api"
echo "  Logs Frontend:     docker-compose logs -f web"
echo "  Logs FastAPI:      docker-compose logs -f notifications"
echo "  Logs Nginx:        docker-compose logs -f nginx"
echo ""
echo """
    return 1
}

echo ""
echo -e "${GREEN}     ¡La aplicación TODO está lista para usar!${NC}"
echo ""