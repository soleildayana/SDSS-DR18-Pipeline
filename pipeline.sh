#!/bin/bash

# Pipeline SDSS-DR18: Descarga → BD Local → Visualización
# Ciencia de Datos Abierta y Reproducible

set -e  # Detener en cualquier error

echo "=========================================="
echo "  PIPELINE: Análisis de Expansión del Universo"
echo "  Datos: SDSS DR18"
echo "=========================================="

# Paso 1: Descarga SQL remota y creación de BD
echo ""
echo "1️⃣  Descargando datos y creando base de datos local..."
python3 constructor_db.py || {
    echo "❌ Error en constructor_db.py"
    exit 1
}

# Paso 2: Análisis visual y generación de gráfico
echo ""
echo "2️⃣  Generando análisis visual..."
python3 analisis_visual.py || {
    echo "❌ Error en analisis_visual.py"
    exit 1
}

# Confirmación final
echo ""
echo "=========================================="
echo "✅ Pipeline completado exitosamente"
echo "=========================================="
echo ""
echo "Archivos generados:"
echo "  📊 resultado.png    — Gráfico Color Index vs Redshift"
echo "  🗄️  datos_mision.db  — Base de datos local SQLite"
echo ""
echo "Próximo paso: Revisar resultado.png y actualizar README.md"
echo "=========================================="
