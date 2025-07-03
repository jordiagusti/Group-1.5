from playwright.sync_api import sync_playwright
import json

# ID del tweet que quieres scrapear
tweet_id = '1864840456326004906'
tweet_url = f'https://x.com/i/web/status/{tweet_id}'

# Cargar cookies
with open('cookies_playwright.json', 'r', encoding='utf-8') as f:
    cookies = json.load(f)

# Usar Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Si quieres ver la ventana, pon headless=False
    context = browser.new_context()
    context.add_cookies(cookies)

    page = context.new_page()
    print(f"✅ Navegando a: {tweet_url}")
    page.goto(tweet_url, timeout=60000)

    # Hacer screenshot
    page.screenshot(path='screenshot.png')
    print("✅ Screenshot guardado como screenshot.png")

    try:
        page.wait_for_selector('article', timeout=10000)  # 10 segundos
        tweet_text = page.inner_text('article')
        print("========== TWEET SCRAPEADO ==========")
        print(tweet_text)
        print("=====================================")
    except Exception as e:
        print("⚠️ No se encontró el artículo del tweet.")
        print("Error:", e)

    browser.close()
