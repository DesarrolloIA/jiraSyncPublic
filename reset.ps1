# Colores para mensajes
$Green = [System.ConsoleColor]::Green
$Yellow = [System.ConsoleColor]::Yellow
$Red = [System.ConsoleColor]::Red

# Función para imprimir mensajes
function Write-Message {
    param($Message)
    Write-Host "[INFO] " -ForegroundColor $Green -NoNewline
    Write-Host $Message
}

function Write-Warning {
    param($Message)
    Write-Host "[WARNING] " -ForegroundColor $Yellow -NoNewline
    Write-Host $Message
}

function Write-Error {
    param($Message)
    Write-Host "[ERROR] " -ForegroundColor $Red -NoNewline
    Write-Host $Message
}

# Función para confirmar acción
function Confirm-Action {
    param($Message)
    $confirmation = Read-Host "$Message [y/N]"
    return $confirmation -eq 'y' -or $confirmation -eq 'Y'
}

# Función para verificar y crear .env
function Check-EnvFile {
    if (-not (Test-Path ".env")) {
        if (Test-Path "env.example") {
            Write-Warning "Archivo .env no encontrado. Creando uno nuevo desde env.example..."
            Copy-Item "env.example" ".env"
            Write-Message "Por favor, edita el archivo .env con tus configuraciones"
            return $false
        } else {
            Write-Error "No se encontró ni .env ni env.example"
            return $false
        }
    }
    return $true
}

# Detener contenedores
function Stop-Containers {
    Write-Message "Deteniendo contenedores..."
    docker compose down
}

# Reiniciar MySQL
function Reset-MySQL {
    Write-Message "Reiniciando datos de MySQL..."
    Remove-Item -Path "volumes\mysql\*" -Force -Recurse -ErrorAction SilentlyContinue
    New-Item -Path "volumes\mysql\.gitkeep" -ItemType File -Force | Out-Null
    Write-Message "Datos de MySQL eliminados"
}

# Reiniciar Backups
function Reset-Backups {
    Write-Message "Reiniciando backups..."
    Remove-Item -Path "volumes\backups\*" -Force -Recurse -ErrorAction SilentlyContinue
    New-Item -Path "volumes\backups\.gitkeep" -ItemType File -Force | Out-Null
    Write-Message "Backups eliminados"
}

# Reiniciar Configuraciones
function Reset-Config {
    Write-Message "Reiniciando configuraciones..."
    # Restaurar configuración por defecto de MySQL
    $mysqlConfig = @"
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
"@
    Set-Content -Path "config\mysql\my.cnf" -Value $mysqlConfig -Force
    Write-Message "Configuraciones restauradas"
}

# Menú principal
function Show-Menu {
    Write-Host "`n=== Jira Sync - Herramienta de Reinicio ===" -ForegroundColor $Green
    Write-Host "1) Reiniciar todo (datos + configuraciones)"
    Write-Host "2) Reiniciar solo datos de MySQL"
    Write-Host "3) Reiniciar solo backups"
    Write-Host "4) Reiniciar configuraciones"
    Write-Host "5) Salir"
}

# Función principal
function Main {
    # Verificar .env antes de continuar
    if (-not (Check-EnvFile)) {
        return
    }

    while ($true) {
        Show-Menu
        $opt = Read-Host "Selecciona una opción"
        switch ($opt) {
            "1" {
                if (Confirm-Action "Esto eliminará TODOS los datos y configuraciones. ¿Estás seguro?") {
                    Stop-Containers
                    Reset-MySQL
                    Reset-Backups
                    Reset-Config
                    Write-Message "Reinicio completo finalizado"
                    Write-Message "Usa 'docker compose up -d' para reiniciar los servicios"
                }
            }
            "2" {
                if (Confirm-Action "Esto eliminará TODOS los datos de MySQL. ¿Estás seguro?") {
                    Stop-Containers
                    Reset-MySQL
                    Write-Message "Reinicio de MySQL finalizado"
                    Write-Message "Usa 'docker compose up -d' para reiniciar los servicios"
                }
            }
            "3" {
                if (Confirm-Action "Esto eliminará TODOS los backups. ¿Estás seguro?") {
                    Reset-Backups
                    Write-Message "Reinicio de backups finalizado"
                }
            }
            "4" {
                if (Confirm-Action "Esto restaurará las configuraciones por defecto. ¿Estás seguro?") {
                    Stop-Containers
                    Reset-Config
                    Write-Message "Reinicio de configuraciones finalizado"
                    Write-Message "Usa 'docker compose up -d' para reiniciar los servicios"
                }
            }
            "5" {
                Write-Message "Saliendo..."
                exit
            }
            default {
                Write-Error "Opción inválida"
            }
        }
    }
}

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "docker-compose.yml")) {
    Write-Error "Este script debe ejecutarse desde el directorio raíz del proyecto"
    exit 1
}

# Ejecutar el menú principal
Main 