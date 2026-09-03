# LIBRERIAS
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Conexión a base de datos local creada en el script anterior
conexion = sqlite3.connect('datos_mision.db')

# Consulta SQL para extraer los datos
consulta = """
SELECT z, g_r, class 
FROM objetos
"""

# Leer la consulta y convertir a DataFrame
data = pd.read_sql_query(consulta, conexion)
conexion.close()

print("--- Datos Cargados desde BD ---")

# Graficar índice de color vs redshift
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))

sns.scatterplot(data=data, x='z', y='g_r', hue='class',
                style='class', palette='Set2', s=70, alpha=0.7)

plt.title('Evidencia de Expansión: Galaxias Locales vs Quásares Lejanos')
plt.xlabel('Redshift (z)')
plt.ylabel('Índice de Color (g - r)')

plt.ylim(-0.5, 2.5)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.axhline(0, color='grey', linewidth=0.8)
plt.legend(title='Clase', loc='best')

# Guardar imagen
plt.tight_layout()
plt.savefig('resultado.png', dpi=300, bbox_inches='tight')

print("\n✓ Imagen 'resultado.png' generada exitosamente.")
