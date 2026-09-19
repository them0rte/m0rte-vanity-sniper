import aiohttp
import asyncio
import json
import os
from datetime import datetime

CONFIG_FILE = "config.json"

# Ayarları yükleyen fonksiyon
def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"[HATA] {CONFIG_FILE} bulunamadı! Lütfen ayarlarınızı yapın.")
        exit(1)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# Ayarları değişkene ata
config = load_config()
TOKEN = config.get("TOKEN")
GUILD_ID = config.get("GUILD_ID")
VANITY_CODE = config.get("VANITY_CODE")
DELAY = config.get("DELAY", 1.0)

HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}
URL = f"https://discord.com/api/v10/guilds/{GUILD_ID}/vanity-url"
PAYLOAD = {"code": VANITY_CODE}

# Terminale saatli ve seviyeli log yazdıran fonksiyon
def log(message, level="BİLGİ"):
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time_str}] [{level}] {message}")

async def snipe_url():
    log(f"Hedef URL: '{VANITY_CODE}' için dinleme başlatıldı...", "BAŞLANGIÇ")
    
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.patch(URL, headers=HEADERS, json=PAYLOAD) as response:
                    if response.status == 200:
                        log(f"URL BAŞARIYLA ALINDI: discord.gg/{VANITY_CODE}", "BAŞARILI")
                        break
                    elif response.status == 429:
                        json_resp = await response.json()
                        retry_after = json_resp.get("retry_after", 1)
                        log(f"Discord Hız Sınırı (Rate Limit). {retry_after} saniye bekleniyor...", "UYARI")
                        await asyncio.sleep(retry_after)
                    else:
                        log(f"Hata Kodu: {response.status} - URL alınamadı, tekrar deneniyor...", "DENEME")
                        await asyncio.sleep(DELAY)
            except Exception as e:
                log(f"Bağlantı hatası veya zaman aşımı: {e}", "HATA")
                await asyncio.sleep(2)  # Hata durumunda yığılmayı önlemek için bekle

if __name__ == "__main__":
    try:
        asyncio.run(snipe_url())
    except KeyboardInterrupt:
        print("\n[İPTAL] İşlem kullanıcı tarafından durduruldu.")
