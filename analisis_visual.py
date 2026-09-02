# LIBRERIAS
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#que se conecte a datos_mision.db, extraiga los datos usando una consulta SQL, realice los cálculos matemáticos y genere una imagen (resultado.png).

# Graficar índice de color vs redshift

plt.style.use('dark_background')

sns.scatterplot(data=data, x='z', y='g_r', hue='class',
                style='class', palette='Set2', s=70)

plt.title('Evidencia de Expansión: Galaxias Locales vs Quásares Lejanos')
plt.xlabel('Redshift (z)')
plt.ylabel('Índice de Color (g - r)')

plt.ylim(-0.5, 2.5)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.axhline(0, color='grey', linewidth=0.8)

plt.show()
