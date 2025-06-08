# Script para verificar archivos de backup en Windows
# check_backups.ps1

Write-Host "=== Verificacion de Archivos de Backup ===" -ForegroundColor Green
Write-Host ""

# Obtener el directorio actual
$currentDir = Get-Location
$backupsDir = Join-Path $currentDir "backups"

Write-Host "Directorio actual: $currentDir" -ForegroundColor Yellow
Write-Host "Directorio de backups: $backupsDir" -ForegroundColor Yellow
Write-Host ""

# Verificar si existe el directorio
if (Test-Path $backupsDir) {
    Write-Host "El directorio de backups existe" -ForegroundColor Green
    
    # Listar archivos SQL
    $sqlFiles = Get-ChildItem -Path $backupsDir -Filter "*.sql" | Sort-Object CreationTime -Descending
    
    if ($sqlFiles.Count -gt 0) {
        Write-Host ""
        Write-Host "Archivos de backup encontrados: $($sqlFiles.Count)" -ForegroundColor Cyan
        Write-Host ("=" * 80)
        
        foreach ($file in $sqlFiles) {
            Write-Host ""
            Write-Host "Archivo: $($file.Name)" -ForegroundColor Yellow
            Write-Host "  Ruta completa: $($file.FullName)"
            $sizeInMB = [math]::Round($file.Length / 1MB, 2)
            Write-Host "  Tamano: $sizeInMB MB"
            Write-Host "  Bytes: $($file.Length)"
            Write-Host "  Creado: $($file.CreationTime)"
            Write-Host "  Modificado: $($file.LastWriteTime)"
            
            # Mostrar las primeras lineas del archivo
            Write-Host "  Primeras 5 lineas:" -ForegroundColor Gray
            try {
                $content = Get-Content $file.FullName -TotalCount 5
                foreach ($line in $content) {
                    Write-Host "    $line" -ForegroundColor DarkGray
                }
            } catch {
                Write-Host "    Error al leer el archivo" -ForegroundColor Red
            }
        }
        
        Write-Host ""
        Write-Host ("=" * 80)
        Write-Host "Resumen:" -ForegroundColor Cyan
        $totalSize = ($sqlFiles | Measure-Object -Property Length -Sum).Sum
        $totalSizeMB = [math]::Round($totalSize / 1MB, 2)
        Write-Host "  Total de archivos: $($sqlFiles.Count)"
        Write-Host "  Tamano total: $totalSizeMB MB"
        if ($sqlFiles.Count -gt 0) {
            Write-Host "  Archivo mas reciente: $($sqlFiles[0].Name)"
            Write-Host "  Archivo mas antiguo: $($sqlFiles[-1].Name)"
        }
        
    } else {
        Write-Host "No se encontraron archivos SQL en el directorio de backups" -ForegroundColor Red
    }
} else {
    Write-Host "El directorio de backups no existe" -ForegroundColor Red
    Write-Host "  Se esperaba en: $backupsDir" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..."
Read-Host 