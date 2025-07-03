import json

# Leer tu cookies_twikit.json actual (diccionario key-value)
with open('cookies_twikit.json', 'r', encoding='utf-8') as f:
    cookies_dict = json.load(f)

# Generar lista de cookies para Playwright
cookies = []
for name, value in cookies_dict.items():
    cookies.append({
        'name': name,
        'value': value,
        'domain': '.x.com',
        'path': '/',
        'expires': -1,
        'httpOnly': False,
        'secure': True,
        'sameSite': 'Lax'
    })

# Guardar en nuevo archivo → cookies_playwright.json
with open('cookies_playwright.json', 'w', encoding='utf-8') as f:
    json.dump(cookies, f, indent=4)

print("✅ Conversión completa → generado: cookies_playwright.json")
