# Análisis de la Expansión del Universo mediante Índice de Color y Redshift
*Análisis reproducible de datos astronómicos públicos*
#### *Soleil Dayana Niño Murcia* | Universidad de Antioquia | **Curso**: Minería de Datos en Astronomía  




Este repositorio aloja el desarrollo de un proyecto de ciencia de datos abierta, cuyo propósito es evidenciar la expansión del universo, mediante el análisis de la relación entre el índice de las bandas de color g-r y el redshift (z) de galaxias y cuásares, observados por el SDSS DR18 (Sloan Digital Sky Survey Data Release 18). 

<img class="imagen-entrada" src="https://github.com/soleildayana/SDSS-DR18-Pipeline/blob/main/resultado.png" alt="Evidencia de expansión del universo: Gráfico índice g-r vs. redshift" >

## Pregunta de Investigación

¿Qué comportamiento sigue la distribución de galaxias locales versus cuásares en función de la relación índice de color - redshift? ¿Qué se puede deducir acerca del universo a partir de dicha relación?   

### Datos: Fuente y Descarga

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

### Limpieza
El CSV descargado contiene estrellas (class = STAR) junto con galaxias y cuásares. Estas son descartadas porque su índice de color no es comparable al de galaxias o cuásares, al no formarse en entornos cosmológicos no se puede pretender evidenciar la expansión cósmica en ellas. 
Así, al aplicar el filtro `class != 'STAR'`, se obtiene un dataset limpio que deja una muestra de alrededor de dos mil objetos (1,941 galaxias + 453 quásares).

### Índice de Color

El índice de color g−r se define como:
$$g-r = m_g - m_r$$

donde $m_g$ y $m_r$ son las magnitudes aparentes en las bandas g y r.

Un valor bajo en este índice (g−r ≈ 0 a 1) indica objetos azules: estrellas jóvenes y baja edad media. Por otro lado, un valor alto (g-r > 1.5) representa objetos rojos, estrellas viejas y de mayor edad media. En el contexto de galaxias, las espirales tienen un g-r bajo por tener población estelar masiva y caliente; mientras que las de g-r alto refieren a una población estelar envejecida. Los **quásares** son muy estudiados por su variabilidad, así que pueden mostrar g−r variable, pero igual tienden a mantenerse en valores muy altos, gracias a la emisión energética de su núcleo activo y el efecto de enrojecimiento por polvo.

### Corrimiento al Rojo (Redshift)

El redshift $z$ mide el desplazamiento de líneas espectrales hacia longitudes de onda mayores, tal que:
- $z$ bajo (z < 0.5): Galaxias del universo local, distancias < 2 Gpc.
- $z$ intermedio (0.5 < z < 2): Universo de edades intermedias.
- $z$ alto (z > 2): Objetos primordiales, universo temprano.

## Análisis de Resultados

En el caso de las galaxias (o azul), podríamos pensar en dos grupos representativos: 
   - **1< g-r <2 y z < 1**: La región más poblada. El g-r alto indica población estelar con edad avanzada, indicio de ser el grupo de galaxias elípticas, masivas y viejas.

   - **z < 0.5 y g-r 0.7 a 1**: Las galaxias más cercanas. Su índice tendiendo más al azul indica formación estelar reciente. Los redshifts casi nulos muestran que residen en nuestro vecindario.
   - 
Note que a partir de g-r = 1, se ve claramente una relación, donde el índice y z aumentan proporcionalmente. Es decir, las galaxias más energéticas y masivas se encuentran en barrios más lejanos.

Ahora, la distribución de cuásares (x roja) predomina notoriamente en g-r menores a 5, su espectro tiende mucho más al rojo. Esto se puede explicar gracias a dos tipos de enrojecimiento, uno generado por lo que llaman columna de densidad, formada por el polvo intergaláctico que nos separa de ellos, que al intermediar en la vista enrrojece su color; segundo, el generado por el efecto Doppler relativista, que también produce este efecto, pero en menor proporción. Los casos que tienden al azul pueden darse tanto por la variabilidad característica de los cuásares, como también por el ángulo de observación, pues al ver de manera más directa el núcleo activo, se observan procesos más energéticos.

En los cuásares el rango del redshift es mucho más extendido, pues eran más comunes en el universo primitivo, cuando había más gas disponible para alimentar agujeros negros supermasivos. Es extremamente sorprendente ver marcas en z > 6, pues significa que observamos cuerpos que existieron cuando el universo tenía ~800 millones de años.

### Conclusiones

1. **Dependencia de z con la distancia**: Objetos con mayor z están más lejos. La existencia de galaxias a z ≈ 0.6 y quásares a z ≈ 7 demuestra que el universo tiene una "profundidad temporal": ver objetos lejanos es ver el pasado.

2. **Ausencia de objetos locales masivos con alto z**: No hay galaxias locales (z ≈ 0) que sean primordiales. Esto es consistente con la expansión: al tener un cuarto más pequeño, todo está más junto y parece ocupar más espacio, mientras que ordenando los mismos objetos en una sala amplia, parecen más pequeños y distantes entre sí; al aplicar esto al universo, las galaxias primordiales tenían mayor material en su vecindario y ópticamente lucen mucho más grandes desde nuestro punto de vista (como ver a través de un cono).

3. **Distribución de edades aparentes**: La región con mayor concentración de galaxias (1< g-r <2 y z < 1) muestra un aumento lineal entre el color g-r y el redshift. Las galaxias de nuestro vecindario tienden a ser menos energéticas a pesar de tener formación estelar reciente. 


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
- **Cosmology Textbook**: Perlmutter & Schmidt (1999) "Measuring Cosmic Acceleration"
- **Clase 4 (Minería de Datos)**: https://esilvavilla.github.io/MineriaDatosweb/Clase_04_SQL_Intro.html 

## 8. Declaración ética de uso de IA

Este proyecto empleó asistencia de herramientas de inteligencia artificial (Github Copilot desde VS). Esta fue empleada en **Debugging**: Asistencia en resolución de errores SSL y optimizaciones de Pandas, y **Convenciones de estilo**: optimización, buenas prácticas. El flujo de trabajo fue diseñado manualmente, toda la interpretación física (galaxias, quásares, redshift, índice de color, cosmología) fue validada manualmente contra fuentes académicas, el análisis es interpretación basada en mis conocimientos de astronomía.

LA IA es una herramienta de productividad. El análisis científico, la crítica y la conclusión son responsabilidad humana.

