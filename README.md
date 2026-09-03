# SDSS-DR18-Pipeline
# Análisis de la Expansión del Universo mediante Índice de Color y Corrimiento al Rojo
**Soleil Dayana Niño Murcia**

Universidad de Antioquia | **Curso**: Minería de Datos en Astronomía  
Análisis reproducible de datos astronómicos públicos 

## 1. Pregunta de Investigación

## 2. Datos: Fuente y Descarga

### Provenance
Los datos provienen del **SDSS DR18** (Data Release 18), un catálogo de objetos astronómicos observados en múltiples bandas fotométricas.

**Endpoint SQL remoto**:
```
https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=csv&cmd=
SELECT TOP 5000 s.class, s.z, p.psfMag_g as g, p.psfMag_r as r 
FROM PhotoObj AS p 
JOIN SpecObj AS s ON p.objid = s.bestobjid
```
## 3. Metodología

## 4. Resultados

## 5. Reproducibilidad: ¿Cómo ejecutar ese proyecto?

### Instalación: 

#### Opción A: Clonar el Repositorio 


```bash
git clone https://github.com/tu-usuario/SDSS-DR18-Pipeline.git
cd SDSS-DR18-Pipeline
```
#### Opción B: Descargar Archivos Directamente

Si prefiere no usar git:

1. Descargar y colocar en una carpeta vacía estos 4 archivos del repositorio:
   - `constructor_db.py`
   - `analisis_visual.py`
   - `pipeline.sh`
   - `README.md` (opcional, para referencia)
    Luego, abrir el terminal en esa carpeta y continuar con los pasos de abajo.

### Requisitos Previos
- **Python 3.8+** instalado.
- Librerías: `pandas`, `sqlite3`, `matplotlib`, `seaborn`.
- Conexión a internet (descarga datos de SDSS).

### Instalación de Librerías
Si no tiene las librerías instaladas, ejecute en su terminal:
```bash
pip install pandas matplotlib seaborn
```

(La librería `sqlite3` viene incluida en Python.)

### Para Reproducir:


```bash
bash pipeline.sh
```

Este script automáticamente:
1. Descarga datos de SDSS DR18
2. Limpia y calcula índice de color
3. Guarda en base de datos local
4. Genera gráfico `resultado.png`
5. **Abre automáticamente la imagen** (confirmar)

**Salida esperada:**
```
==========================================
  PIPELINE: Análisis de Expansión del Universo
  Datos: SDSS DR18
==========================================

1️⃣  Descargando datos y creando base de datos local...
Descargando datos de SDSS DR18...
✓ Base de datos 'datos_mision.db' creada exitosamente.

2️⃣  Generando análisis visual...
✓ Imagen 'resultado.png' generada exitosamente.

==========================================
✅ Pipeline completado exitosamente
==========================================
```

---

## 6. Estructura del Repositorio

## 7. Referencias y Lecturas Complementarias

- **SDSS Data Release 18**: https://www.sdss.org/dr18/
- **SkyServer SQL API**: https://skyserver.sdss.org/dr18/en/tools/search/sql
- **Cosmology Textbook**: Perlmutter & Schmidt (1999) "Measuring Cosmic Acceleration"
- **Clase 4 (Minería de Datos)**: https://esilvavilla.github.io/MineriaDatosweb/Clase_04_SQL_Intro.html

## 8. Declaración ética de uso de IA
