#!/bin/bash

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para confirmar acción
confirm_action() {
    read -p "$(echo -e ${YELLOW}[WARNING]${NC} $1 [y/N]: )" -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        return 1
    fi
    return 0
}

# Función para verificar y crear .env
check_env_file() {
    if [ ! -f ".env" ]; then
        if [ -f "env.example" ]; then
            print_warning "Archivo .env no encontrado. Creando uno nuevo desde env.example..."
            cp env.example .env
            print_message "Por favor, edita el archivo .env con tus configuraciones"
            return 1
        else
            print_error "No se encontró ni .env ni env.example"
            return 1
        fi
    fi
    return 0
}

# Detener contenedores
stop_containers() {
    print_message "Deteniendo contenedores..."
    docker compose down
}

# Reiniciar MySQL
reset_mysql() {
    print_message "Reiniciando datos de MySQL..."
    # Intentar primero sin sudo
    if ! rm -rf volumes/mysql/* 2>/dev/null; then
        print_warning "Se requieren permisos de superusuario para limpiar MySQL"
        sudo rm -rf volumes/mysql/*
    fi
    touch volumes/mysql/.gitkeep
    print_message "Datos de MySQL eliminados"
}

# Reiniciar Backups
reset_backups() {
    print_message "Reiniciando backups..."
    rm -rf volumes/backups/*
    touch volumes/backups/.gitkeep
    print_message "Backups eliminados"
}

# Reiniciar Configuraciones
reset_config() {
    print_message "Reiniciando configuraciones..."
    # Restaurar configuración por defecto de MySQL
    cat > config/mysql/my.cnf << EOL
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
max_connections = 150
max_allowed_packet = 64M
innodb_buffer_pool_size = 256M
innodb_log_file_size = 64M
slow_query_log = 1
long_query_time = 2
slow_query_log_file = /var/lib/mysql/mysql-slow.log

[client]
default-character-set = utf8mb4
EOL
    print_message "Configuraciones restauradas"
}

# Menú principal
show_menu() {
    echo -e "\n${GREEN}=== Jira Sync - Herramienta de Reinicio ===${NC}"
    echo "1) Reiniciar todo (datos + configuraciones)"
    echo "2) Reiniciar solo datos de MySQL"
    echo "3) Reiniciar solo backups"
    echo "4) Reiniciar configuraciones"
    echo "5) Salir"
}

# Función principal
main() {
    # Verificar .env antes de continuar
    check_env_file || return 1

    while true; do
        show_menu
        read -p "Selecciona una opción: " opt
        case $opt in
            1)
                if confirm_action "Esto eliminará TODOS los datos y configuraciones. ¿Estás seguro?"; then
                    stop_containers
                    reset_mysql
                    reset_backups
                    reset_config
                    print_message "Reinicio completo finalizado"
                    print_message "Usa 'docker compose up -d' para reiniciar los servicios"
                fi
                ;;
            2)
                if confirm_action "Esto eliminará TODOS los datos de MySQL. ¿Estás seguro?"; then
                    stop_containers
                    reset_mysql
                    print_message "Reinicio de MySQL finalizado"
                    print_message "Usa 'docker compose up -d' para reiniciar los servicios"
                fi
                ;;
            3)
                if confirm_action "Esto eliminará TODOS los backups. ¿Estás seguro?"; then
                    reset_backups
                    print_message "Reinicio de backups finalizado"
                fi
                ;;
            4)
                if confirm_action "Esto restaurará las configuraciones por defecto. ¿Estás seguro?"; then
                    stop_containers
                    reset_config
                    print_message "Reinicio de configuraciones finalizado"
                    print_message "Usa 'docker compose up -d' para reiniciar los servicios"
                fi
                ;;
            5)
                print_message "Saliendo..."
                exit 0
                ;;
            *)
                print_error "Opción inválida"
                ;;
        esac
    done
}

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    print_error "Este script debe ejecutarse desde el directorio raíz del proyecto"
    exit 1
fi

# Ejecutar el menú principal
main 