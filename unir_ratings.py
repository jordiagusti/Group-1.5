import os
import pandas as pd

# Ruta donde están los .tsv descomprimidos
folder_path = r'C:\Users\mfmpi\ratings_zips\descomprimidos'

# Lista de dataframes
dfs = []

# Leer todos los .tsv
for file_name in os.listdir(folder_path):
    if file_name.endswith('.tsv'):
        file_path = os.path.join(folder_path, file_name)
        try:
            df = pd.read_csv(file_path, sep='\t', low_memory=False)
            dfs.append(df)
            print(f"✅ Cargado: {file_name} ({len(df)} filas)")
        except Exception as e:
            print(f"⚠️ Error al cargar {file_name}: {e}")

# Unir todos en uno solo
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"\n🧩 Total de filas combinadas: {len(combined_df)}")

    # Guardar en CSV
    output_path = os.path.join(folder_path, 'all_note_ratings.csv')
    combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"💾 CSV guardado en: {output_path}")
else:
    print("❌ No se encontraron archivos TSV válidos.")
