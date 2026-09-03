# SDSS-DR18-Pipeline
# Análisis de la Expansión del Universo mediante Índice de Color y Redshift
**Soleil Dayana Niño Murcia**

Universidad de Antioquia | **Curso**: Minería de Datos en Astronomía  
Análisis reproducible de datos astronómicos públicos 

Este repositorio aloja el desarrollo de un proyecto de ciencia de datos abierta, cuyo propósito es evidenciar la expansión del universo mediante el análisis de la relación entre el índice de las bandas de color g-r y el redshift (z) de galaxias y cuásares observados por el SDSS DR18 (Sloan Digital Sky Survey Data Release 18). 

## 1. Pregunta de Investigación

¿Qué comportamiento sigue la distribución de galaxias locales versus cuásares en función de la relación índice de color - redshift? ¿Qué se puede deducir acerca del universo a partir de dicho comportamiento?   

## 2. Datos: Fuente y Descarga

### Provenance
Los datos provienen del **SDSS DR18**, un catálogo de objetos astronómicos observados en múltiples bandas fotométricas. 
El survey cuenta con múltiples tablas de acceso público; para el caso de este proyecto, son de especial interés dos tablas: *PhotoObj* (fotometría, para rescatar los índices de color) y *SpecObj* (espectroscopía, para obtener redshift y clase). Para tomar las coincidencias entre ambas tablas, se emplea el comando JOIN dentro del query, que combina los datos basándose en la columna de ID. Para esto, fue necesario renombrar una de las columnas de ID, de manera que el nombre fuese el mismo en ambas tablas, y asociar un llamado a cada una de ellas, para indicar dónde se aloja cada elemento solicitado (ej. PhotoObj AS p  --> p.objid).

[**Endpoint SQL remoto**](https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=csv&cmd=)

**Query**: 
```
https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=csv&cmd=
SELECT TOP 5000 s.class, s.z, p.psfMag_g as g, p.psfMag_r as r 
FROM PhotoObj AS p 
JOIN SpecObj AS s ON p.objid = s.bestobjid
```

**Acerca de la consulta**:
- `PhotoObj`: Tabla de fotometría (magnitudes en bandas u, g, r, i, z).
- `SpecObj`: Tabla de espectroscopia (redshift z, clasificación de objeto).
- `JOIN`: Vincula espectro a medidas fotométricas de los objetos según ID.
- `psfMag_g`, `psfMag_r`: Magnitudes PSF (Point Spread Function) en bandas g y r.
- `s.class`: Clasificación (GALAXY, QSO, o STAR).
- `s.z`: Redshift espectroscópico.
- Se seleccionan 5000 objetos.

## 3. Metodología

### 3.1 Limpieza
El CSV descargado contiene estrellas (class = STAR) junto con galaxias y cuásares. Estas son descartadas porque su índice de color no es comparable al de galaxias o cuásares, al no formarse en entornos cosmológicos no se puede pretender evidenciar la expansión cósmica en ellas. 
Así, al aplicar el filtro `class != 'STAR'`, se obtiene un dataset limpio que deja una muestra de alrededor de dos mil objetos (1,941 galaxias + 453 quásares).

### 3.2 Índice de Color

El índice de color g−r se define como:
$$g-r = m_g - m_r$$

donde $m_g$ y $m_r$ son las magnitudes aparentes en las bandas g y r.

Un valor bajo en este índice (g−r ≈ 0 a 1) indica objetos azules: estrellas jóvenes y baja edad media. Por otro lado, un valor alto (g-r > 1.5) representa objetos rojos, estrellas viejas y de mayor edad media. En el contexto de galaxias, las espirales tienen un g-r bajo por tener población estelar masiva y caliente; mientras que las de g-r alto refieren a una población estelar envejecida. Los **quásares** son muy estudiados por su variabilidad, así que pueden mostrar g−r variable, pero igual tienden a mantenerse en valores muy altos, gracias a la emisión energética de su núcleo activo y el efecto de enrojecimiento por polvo.

### 3.3 Corrimiento al Rojo (Redshift)

El redshift $z$ mide el desplazamiento de líneas espectrales hacia longitudes de onda mayores, tal que:
- $z$ bajo (z < 0.5): Galaxias del universo local, distancias < 2 Gpc.
- $z$ intermedio (0.5 < z < 2): Universo de edades intermedias.
- $z$ alto (z > 2): Objetos primordiales, universo temprano.


## 4. Resultados

## 5. ¿Cómo ejecutar ese proyecto?

### Instalación: 

#### Opción A: Clonar el Repositorio 

```bash
git clone https://github.com/soleildayana/SDSS-DR18-Pipeline.git
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
Ejecutar el Pipeline completo con el comando:
```bash
bash pipeline.sh
```

Este script automáticamente:
1. Descarga datos de SDSS DR18
2. Limpia y calcula índice de color
3. Guarda `datos_mision.db` en base de datos SQLite local
4. Genera gráfico `resultado.png`

Una vez reproducido, se recomienda visualizar el gráfico `resultado.png`.

---

## 6. Estructura del Repositorio

## 7. Referencias y Lecturas Complementarias

- **SDSS Data Release 18**: https://www.sdss.org/dr18/
- **SkyServer SQL API**: https://skyserver.sdss.org/dr18/en/tools/search/sql
- **Cosmology Textbook**: Perlmutter & Schmidt (1999) "Measuring Cosmic Acceleration"
- **Clase 4 (Minería de Datos)**: https://esilvavilla.github.io/MineriaDatosweb/Clase_04_SQL_Intro.html

## 8. Declaración ética de uso de IA
