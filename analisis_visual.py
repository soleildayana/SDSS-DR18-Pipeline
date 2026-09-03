# LIBRERIAS
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Conexión a base de datos local (patrón Clase 4)
conexion = sqlite3.connect('datos_mision.db')

# 2. Consulta SQL para extraer datos con filtros
consulta = """
SELECT z, g_r, class 
FROM objetos
"""

# 3. Pandas ejecuta la consulta y convierte a DataFrame
data = pd.read_sql_query(consulta, conexion)
conexion.close()

# 4. Validación de datos post-lectura
print("--- Datos Cargados desde BD ---")
print(f"Registros extraídos: {len(data)}")
print(f"\nValores nulos:")
print(data.isnull().sum())
print(f"\nEstadísticas:")
print(data.describe())
print(f"\nDistribución por clase:")
print(data['class'].value_counts())

# 5. Graficar índice de color vs redshift
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

# 6. Guardar imagen con alta resolución
plt.tight_layout()
plt.savefig('resultado.png', dpi=300, bbox_inches='tight')

print("\n✓ Imagen 'resultado.png' generada exitosamente.")
