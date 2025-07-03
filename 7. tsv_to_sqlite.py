import os
import pandas as pd
import sqlite3

# Ruta a tu carpeta con los ratings descomprimidos
tsv_folder = r'C:\Users\mfmpi\ratings_zips\descomprimidos'

# Crear/conectar a la base de datos SQLite
conn = sqlite3.connect('community_notes_ratings.db')
cursor = conn.cursor()

# Nombre de la tabla
table_name = 'ratings'

# Procesar cada .tsv
for file_name in os.listdir(tsv_folder):
    if file_name.endswith('.tsv'):
        file_path = os.path.join(tsv_folder, file_name)
        try:
            print(f'📥 Leyendo {file_name}...')
            df = pd.read_csv(file_path, sep='\t', low_memory=False)

            # Escribir en SQLite
            df.to_sql(table_name, conn, if_exists='append', index=False)
            print(f'✅ Insertado: {len(df)} filas')
        except Exception as e:
            print(f'⚠️ Error al procesar {file_name}: {e}')

# Cerrar conexión
conn.close()
print('🎉 ¡Base de datos creada con éxito!')
