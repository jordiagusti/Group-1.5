import zipfile
import os
from pathlib import Path

# 👉 CAMBIA esta ruta por donde tienes los .zip en tu PC
zip_folder = Path("C:/Users/mfmpi/ratings_zips")
output_folder = zip_folder / "descomprimidos"
output_folder.mkdir(exist_ok=True)

# Recorre todos los ZIP y los descomprime
for zip_file in zip_folder.glob("*.zip"):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
        print(f"✅ Descomprimido: {zip_file.name}")

print("🚀 Todos los ZIP han sido descomprimidos.")
