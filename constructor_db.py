# LIBRERIAS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Accedemos a la base de datos para leer el csv crudo
url = 'https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=csv&cmd=SELECT%20TOP%205000%20s.class%2C%20s.z%2C%20p.psfMag_g%20as%20g%2C%20p.psfMag_r%20as%20r%20FROM%20PhotoObj%20AS%20p%20JOIN%20SpecObj%20AS%20s%20ON%20p.objid%20%3D%20s.bestobjid'
data = pd.read_csv(url, skiprows=[0]) # Se omite la primera fila ya que es el nombre de la tabla. Si no se hace este paso, la tabla queda como una única columna de nombre '#Table1'

# Eliminar objetos de clase STAR
for index, row in data.iterrows():
    if row['class'] == 'STAR':
        data.drop(index, inplace=True)

# Calcular el índice g - r
data['g_r'] = data['g'] - data['r']

#  Pendiente de guardar los datos procesados en base de datos local SQLite
