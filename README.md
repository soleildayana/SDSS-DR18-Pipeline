<div align="center">

# Análisis de la Expansión del Universo mediante Índice de Color y Redshift
### *Análisis reproducible de datos astronómicos públicos*

**Soleil Dayana Niño Murcia**
Universidad de Antioquia · Curso: Minería de Datos en Astronomía

---

</div>

Este repositorio aloja el desarrollo de un proyecto de ciencia de datos abierta, cuyo propósito es evidenciar la expansión del universo mediante el análisis de la relación entre el índice de las bandas de color g-r y el redshift (z) de galaxias y cuásares, observados por el SDSS DR18 (Sloan Digital Sky Survey Data Release 18).

<p align="center">
<img src="https://github.com/soleildayana/SDSS-DR18-Pipeline/blob/main/resultado.png" alt="Evidencia de expansión del universo: Gráfico índice g-r vs. redshift" width="720">
</p>

## Pregunta de Investigación

¿Qué comportamiento sigue la distribución de galaxias locales versus cuásares en función de la relación índice de color - redshift? ¿Qué se puede deducir acerca del universo a partir de dicha relación?

### Datos: Fuente y Descarga

Los datos provienen del **SDSS DR18**, un catálogo de objetos astronómicos observados en múltiples bandas fotométricas. El survey cuenta con múltiples tablas de acceso público; para este proyecto interesan dos en particular: *PhotoObj* (fotometría, de donde se rescatan los índices de color) y *SpecObj* (espectroscopía, de donde se obtienen el redshift y la clase del objeto). Para tomar las coincidencias entre ambas tablas se emplea un `JOIN` dentro del query, que las combina basándose en la columna de ID; para esto fue necesario renombrar una de las columnas de manera que el nombre coincidiera en ambas tablas, y asociar un alias a cada una para indicar dónde se aloja cada elemento solicitado (ej. `PhotoObj AS p` → `p.objid`).

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

La descarga en sí ocurre dentro de `constructor_db.py`, que lee el CSV directamente desde la URL remota con Pandas; `pipeline.sh` orquesta la secuencia completa (descarga → construcción de base de datos → graficación) pero delega la obtención del dato a Python en lugar de resolverla con `wget` en Bash. Fue una decisión práctica más que una limitación: mantener la lógica de descarga junto a la limpieza en un mismo script evitó duplicar el manejo de errores de red en dos lenguajes distintos.

Vale la pena señalar también que la consulta trae los primeros 5000 registros sin un criterio de aleatorización explícito (no hay `ORDER BY` sobre un campo aleatorio). Esto no invalida el análisis, pues la relación color-redshift que se observa es consistente con la literatura; pero sí significa que la muestra no está garantizada como representativa, ya que la proporción final entre galaxias y cuásares refleja en parte el orden interno de la base de datos, no su abundancia relativa en el cielo.

### Limpieza

El CSV descargado contiene estrellas (`class = STAR`) junto con galaxias y cuásares. Estas se descartan porque su índice de color no es comparable al de galaxias o cuásares, al no formarse en entornos cosmológicos, no tiene sentido buscar en ellas evidencia de expansión cósmica. Al aplicar el filtro `class != 'STAR'` se obtiene un dataset limpio de alrededor de dos mil objetos: 1,941 galaxias y 453 quásares. Esa diferencia de casi un orden de magnitud entre ambas clases es un reflejo —amplificado por la falta de aleatorización mencionada arriba— de que los cuásares son intrínsecamente mucho más raros por grado cuadrado de cielo que las galaxias; con todo, 453 objetos siguen siendo suficientes para reconocer el patrón que describe la literatura (el estudio clásico de Richards et al. 2001 sobre colores de cuásares en SDSS trabajó con apenas 2,625 objetos y logró establecer la relación color-redshift que aquí se reproduce).

Hay una decisión metodológica que conviene dejar clara: la consulta usa magnitudes PSF (`psfMag`) para ambas clases. Esta elección favorece a los cuásares, que son fuentes puntuales, pero subestima el flujo real de las galaxias, que son fuentes extendidas cuya luz se dispersa más allá del perfil PSF ajustado. 

### Índice de Color

El índice de color g−r se define como:
$$g-r = m_g - m_r$$

donde $m_g$ y $m_r$ son las magnitudes aparentes en las bandas g y r.

Un valor bajo en este índice (g−r ≈ 0 a 1) indica objetos azules, de estrellas jóvenes y baja edad media; un valor alto (g-r > 1.5) representa objetos rojos, de estrellas viejas. En galaxias, las espirales tienden a un g-r bajo por su población estelar masiva y caliente, mientras que un g-r alto refiere a una población estelar envejecida. Los cuásares, por su parte, son muy estudiados por su variabilidad, así que pueden mostrar g−r cambiante, pero tienden a mantenerse en valores altos gracias a la emisión energética de su núcleo activo y al enrojecimiento por polvo.

### Corrimiento al Rojo (Redshift)

El redshift $z$ mide el desplazamiento de líneas espectrales hacia longitudes de onda mayores. Como referencia aproximada: z bajo (z < 0.5) corresponde a galaxias del universo local, a distancias menores a 2 Gpc; z intermedio (0.5 < z < 2) a un universo de edades intermedias; y z alto (z > 2) a objetos primordiales del universo temprano.

## Análisis de Resultados

El gráfico separa con bastante claridad dos comportamientos. Las galaxias ocupan casi en su totalidad la franja de z bajo, formando una columna compacta que rara vez sobrepasa z = 1, mientras que los cuásares se extienden libremente hasta z ≈ 7. Esa sola diferencia de rango ya es evidencia directa de la relación distancia-redshift: solo objetos extraordinariamente luminosos, como los núcleos activos de galaxias que alimentan a los cuásares, son visibles a esas distancias, mientras que las galaxias "normales" del catálogo espectroscópico de SDSS solo se detectan cuando están relativamente cerca.

Dentro de la nube de galaxias se percibe un comportamiento curioso, el color g-r no crece de forma monótona con z, sino que sube y luego se dobla, dibujando algo parecido a una "n" en el tramo de z bajo. Esto ocurre por el llamado *4000 Å break*, una caída abrupta de flujo causada por la acumulación de líneas de absorción metálicas en estrellas viejas, que se va desplazando hacia el rojo junto con la galaxia. Mientras ese quiebre cae dentro de la banda g pero todavía no alcanza la banda r, suprime el flujo azul de forma desproporcionada y el color se enrojece rápidamente; una vez el break termina de cruzar hacia r y empieza a afectar a ambas bandas de manera más pareja, el contraste entre ellas se reduce y la curva pierde pendiente. Es, en esencia, el mismo tipo de fenómeno —una característica espectral fija atravesando un sistema de filtros fijo— que después se vuelve a ver, de forma mucho más marcada, en los cuásares.

La distribución de los cuásares dibuja su propio patrón distintivo: el color desciende hasta un mínimo alrededor de z ≈ 2-3 y luego vuelve a subir con fuerza hacia redshifts mayores. Este comportamiento está documentado desde el trabajo fundacional de Richards et al. (2001) sobre colores de cuásares en SDSS, que explicó las variaciones de color con el redshift como el resultado de líneas de emisión anchas —Lyman-α, C IV, Mg II, entre otras— desplazándose dentro y fuera de las bandas fotométricas a medida que z aumenta. La subida final, la más pronunciada, tiene una causa distinta y bien identificada por trabajos posteriores (Fan, 1999): a partir de z ≈ 2, el bosque de Lyman-α y los sistemas Lyman-limit —nubes de gas intergaláctico que absorben fotones en el camino hacia nosotros— empiezan a devorar progresivamente el flujo azul del cuásar en la banda g. El objeto no se ha vuelto físicamente más rojo; lo que ocurre es que el universo que hay entre el cuásar y el telescopio le está filtrando la luz azul antes de que llegue. Vale la pena anotar, además, que la escasez de puntos en z > 5 no es evidencia de que esos objetos dejen de existir, sino un efecto de selección: los cuásares tan distantes son intrínsecamente raros y su detección exige muestras mucho más profundas que las de este catálogo.

### Conclusiones

La primera conclusión, y la más directa, es que la existencia misma de galaxias detectadas hasta z ≈ 0.6 y cuásares hasta z ≈ 7 confirma que el universo tiene una profundidad temporal medible: observar un objeto lejano es, literalmente, observar una versión más joven del universo. Y es fascinante poder observar cuásares en z mayores a 6, pues emitieron su potente luz cuando el universo tenía apenas unos cientos de millones de años, y esa luz ha viajado desde entonces hasta cruzarse con nosotros.

La segunda es la ausencia notable de objetos locales masivos con alto redshift: no hay, en esta muestra ni en ninguna otra, galaxias cercanas que sean a la vez primordiales. Esto es consistente con un universo en expansión, donde el volumen disponible para la materia ha ido creciendo con el tiempo; los objetos que vemos a gran distancia no solo están lejos en el espacio, están lejos en el tiempo, observados en una época en que el universo era más pequeño y denso.

Por último, se concluye que la región de mayor concentración de galaxias muestra una relación creciente entre color y redshift hasta que el 4000 Å break termina de atravesar el sistema de filtros, momento en el que la relación se aplana. Las galaxias del vecindario cósmico —las de z casi nulo— tienden a mostrar colores más azules, indicio de formación estelar todavía activa, mientras que las levemente más distantes dentro de esta misma muestra ya aparecen dominadas por poblaciones estelares más viejas y menos energéticas.

Queda como limitación abierta, y como posible extensión de este trabajo, resolver el desbalance entre clases mediante consultas separadas para galaxias y cuásares (en vez de un único `JOIN` con `TOP N` compartido), e incorporar un muestreo aleatorio explícito que garantice representatividad estadística frente al catálogo completo de DR18.

## ¿Cómo ejecutar ese proyecto?

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

## Estructura del Repositorio

```
SDSS-DR18-Pipeline/
├── constructor_db.py          # Descarga, limpia, almacena en SQLite
├── analisis_visual.py         # Lee BD, grafica, genera PNG
├── pipeline.sh                # Script Bash que orquesta todo
├── README.md                  # Este archivo
├── datos_mision.db            # [Generado] Base de datos SQLite
└── resultado.png              # [Generado] Gráfico final
```

## Referencias

- **SDSS Data Release 18**: https://www.sdss.org/dr18/
- **SkyServer SQL API**: https://skyserver.sdss.org/dr18/en/tools/search/sql
- **Richards, G. T. et al. (2001)**, "Colors of 2625 Quasars at 0<z<5 Measured in the Sloan Digital Sky Survey Photometric System", *The Astronomical Journal*.
- **Fan, X. (1999)**, sobre la dependencia de los colores de cuásares con el redshift en el sistema de filtros de SDSS.
- **Cosmology Textbook**: Perlmutter & Schmidt (1999) "Measuring Cosmic Acceleration"
- **Clase 4 (Minería de Datos)**: https://esilvavilla.github.io/MineriaDatosweb/Clase_04_SQL_Intro.html

## Declaración ética de uso de IA

Este proyecto empleó asistencia de herramientas de inteligencia artificial (Github Copilot desde VS). Esta fue empleada en debugging (resolución de errores SSL y optimizaciones de Pandas) y convenciones de estilo. El flujo de trabajo fue diseñado manualmente, y toda la interpretación física —galaxias, cuásares, redshift, índice de color, cosmología— fue validada contra fuentes académicas y decidida por mí (amor eterno al mundo de los AGNs).

La IA es una herramienta de productividad. El análisis científico, la crítica y la conclusión son responsabilidad humana.
