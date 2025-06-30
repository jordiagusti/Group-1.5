from playwright.sync_api import sync_playwright
import json
import time
import pandas as pd

# ======= CARGAR LISTA DE TWEETS DESDE CSV =======
import csv
tweet_ids = []

with open("muestra_5000.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tweet_ids.append(row["tweet_id"])

print(f"✅ Total de tweets a scrapear: {len(tweet_ids)}")

# ======= CARGAR COOKIES =======
with open('cookies_playwright.json', 'r', encoding='utf-8') as f:
    cookies_raw = json.load(f)

cookies = []
for c in cookies_raw:
    cookies.append({
        'name': c['name'],
        'value': c['value'],
        'domain': c['domain'],
        'path': c['path'],
        'expires': int(c['expirationDate']) if 'expirationDate' in c else -1,
        'httpOnly': c.get('httpOnly', False),
        'secure': c.get('secure', False),
        'sameSite': 'Lax'
    })

# ======= SCRAPING =======
tweets_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    context.add_cookies(cookies)
    page = context.new_page()

    for i, tweet_id in enumerate(tweet_ids):
        tweet_url = f'https://x.com/i/web/status/{tweet_id}'
        print(f"➡️ ({i+1}/{len(tweet_ids)}) Navegando a: {tweet_url}")

        try:
            page.goto(tweet_url)
            page.wait_for_selector('article', timeout=10000)  # 10 seg
            tweet_text = page.inner_text('article')

            print(f"✅ Scrapeado tweet_id: {tweet_id}")
            tweets_data.append({
                'tweet_id': tweet_id,
                'tweet_url': tweet_url,
                'tweet_text': tweet_text
            })

        except Exception as e:
            print(f"⚠️ Error en tweet_id: {tweet_id} → {str(e)}")
            tweets_data.append({
                'tweet_id': tweet_id,
                'tweet_url': tweet_url,
                'tweet_text': 'ERROR'
            })

        time.sleep(1)  # Evitar bloqueos por velocidad

    browser.close()

# ======= GUARDAR CSV =======
df_out = pd.DataFrame(tweets_data)
df_out.to_csv('tweets_scrape.csv', index=False, encoding='utf-8-sig')

print("🚀 Scraping terminado → resultados guardados en: tweets_scrape.csv")
