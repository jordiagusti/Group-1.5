import pandas as pd
import os

# Rutas locales
ratings_path = r'C:\Users\mfmpi\notas_con_ratings.csv'
enrollment_path = r'C:\Users\mfmpi\userEnrollment-00000.tsv'
output_path = r'C:\Users\mfmpi\notas_con_ratings_y_usuarios.csv'

# Verificar existencia
if not os.path.exists(ratings_path):
    raise FileNotFoundError(f"❌ No se encuentra el archivo: {ratings_path}")
if not os.path.exists(enrollment_path):
    raise FileNotFoundError(f"❌ No se encuentra el archivo: {enrollment_path}")

# Cargar archivo de usuarios
df_users = pd.read_csv(enrollment_path, sep='\t')
print(f"✅ Usuarios cargados: {df_users.shape}")

# Leer CSV grande en bloques
chunk_size = 50000
chunks = pd.read_csv(ratings_path, chunksize=chunk_size)
result_chunks = []

for i, chunk in enumerate(chunks):
    print(f"🔹 Procesando bloque {i+1} con {len(chunk)} filas...")
    # Merge con usuarios
    merged = chunk.merge(df_users, left_on='raterParticipantId', right_on='participantId', how='left')
    result_chunks.append(merged)
    print(f"✅ Bloque {i+1} unido: {merged.shape[0]} filas")

# Concatenar todo y guardar
df_final = pd.concat(result_chunks, ignore_index=True)
df_final.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\n🎉 Unión completada: {df_final.shape[0]} filas guardadas en '{output_path}'")
