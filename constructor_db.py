# LIBRERIAS
import pandas as pd
import sqlite3

# Descarga SQL remota desde SDSS DR18
url = 'https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=csv&cmd=SELECT%20TOP%205000%20s.class%2C%20s.z%2C%20p.psfMag_g%20as%20g%2C%20p.psfMag_r%20as%20r%20FROM%20PhotoObj%20AS%20p%20JOIN%20SpecObj%20AS%20s%20ON%20p.objid%20%3D%20s.bestobjid'
data = pd.read_csv(url, skiprows=[0])

# Eliminar objetos de clase STAR (no son galaxias ni quásares)
data = data[data['class'] != 'STAR'].reset_index(drop=True)

# Calcular índice de color g - r
data['g_r'] = data['g'] - data['r']

print(f"\nDistribución por clase:")
print(data['class'].value_counts())

# Migrar a SQLite local
conexion = sqlite3.connect('datos_mision.db')
data.to_sql('objetos', conexion, if_exists='replace', index=True)
conexion.close()

print("\n✓ Base de datos 'datos_mision.db' creada exitosamente.")
