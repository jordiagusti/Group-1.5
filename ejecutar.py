import pandas as pd
import sqlite3
import os

# Rutas locales
csv_path = r'C:\Users\mfmpi\merged_intermediate_df.csv'
db_path = r'C:\Users\mfmpi\community_notes_ratings.db'
output_path = r'C:\Users\mfmpi\notas_con_ratings.csv'

# Verificar existencia de archivos
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"No se encuentra el archivo CSV: {csv_path}")
if not os.path.exists(db_path):
    raise FileNotFoundError(f"No se encuentra la base de datos: {db_path}")

# Conectar a SQLite
conn = sqlite3.connect(db_path)
print("✅ Conectado a la base de datos.")

# Crear índice en noteId para optimizar
conn.execute("CREATE INDEX IF NOT EXISTS idx_noteId ON ratings(noteId)")

# Columnas deseadas de ratings
ratings_columns = [
    "noteId",
    "raterParticipantId",
    "createdAtMillis AS ratingCreatedAtMillis",
    "agree", "disagree",
    "helpfulnessLevel",
    "helpfulOther", "helpfulClear", "helpfulGoodSources", "helpfulAddressesClaim",
    "notHelpfulOther", "notHelpfulIncorrect", "notHelpfulSourcesMissingOrUnreliable",
    "notHelpfulMissingKeyPoints", "notHelpfulHardToUnderstand",
    "notHelpfulArgumentativeOrBiased", "notHelpfulSpamHarassmentOrAbuse",
    "notHelpfulIrrelevantSources", "notHelpfulOpinionSpeculation", "notHelpfulNoteNotNeeded"
]

select_clause = ",\n  r.".join(["n.*"] + ratings_columns)

# Subir CSV como tabla temporal y procesar por bloques
chunk_size = 500
df_iter = pd.read_csv(csv_path, chunksize=chunk_size)
all_chunks = []

for i, chunk in enumerate(df_iter):
    print(f"🔹 Procesando bloque {i+1} con {len(chunk)} filas...")
    chunk.to_sql("notes_temp", conn, if_exists="replace", index=False)

    query = f"""
    SELECT
      {select_clause}
    FROM notes_temp n
    LEFT JOIN ratings r ON n.noteId = r.noteId
    """
    result = pd.read_sql_query(query, conn)
    all_chunks.append(result)
    print(f"✅ Bloque {i+1} unido: {result.shape[0]} filas")

# Concatenar todos los bloques
df_final = pd.concat(all_chunks, ignore_index=True)
df_final.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"🎉 Exportación final completada: {df_final.shape[0]} filas guardadas en '{output_path}'")
