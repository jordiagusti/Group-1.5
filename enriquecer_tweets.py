import pandas as pd
import re

# Cargar el CSV original
df = pd.read_csv('tweets_scrape.csv')

# Función para extraer métricas
def extraer_metricas(texto):
    try:
        partes = texto.strip().split('\n')[-6:]
        numeros = []

        for parte in partes:
            match = re.search(r'([\d.,]+)([KM]?)', parte)
            if match:
                num, sufijo = match.groups()
                num = num.replace(',', '')
                if sufijo == 'K':
                    valor = float(num) * 1_000
                elif sufijo == 'M':
                    valor = float(num) * 1_000_000
                else:
                    valor = float(num)
                numeros.append(int(valor))

        while len(numeros) < 5:
            numeros.insert(0, None)

        return pd.Series(numeros[-5:], index=['views', 'replies', 'reposts', 'likes', 'bookmarks'])

    except:
        return pd.Series([None]*5, index=['views', 'replies', 'reposts', 'likes', 'bookmarks'])

# Función para extraer la fecha (sin hora)
def extraer_fecha(texto):
    patron = r"\d{1,2}:\d{2} [AP]M · [A-Za-z]{3,9} \d{1,2}, \d{4}"
    match = re.search(patron, texto)
    if match:
        fecha_str = match.group(0)
        try:
            fecha = pd.to_datetime(fecha_str, errors='coerce')
            return fecha.date() if pd.notnull(fecha) else None
        except:
            return None
    return None

# Aplicar funciones
df[['views', 'replies', 'reposts', 'likes', 'bookmarks']] = df['tweet_text'].apply(extraer_metricas)
df['fecha'] = df['tweet_text'].apply(extraer_fecha)

# Guardar el nuevo CSV
df.to_csv('tweets_scrape_enriquecido.csv', index=False, encoding='utf-8-sig')
print("✅ Archivo enriquecido guardado como tweets_scrape_enriquecido.csv")
