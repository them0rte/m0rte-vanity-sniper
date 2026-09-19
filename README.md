# Discord Vanity URL Sniper (M0RTE)

Bu proje, silinen veya boşa düşen Discord özel URL'lerini (vanity URL) asenkron olarak en hızlı şekilde kendi sunucunuza almanızı sağlayan, VDS ve PM2 uyumlu bir Python scriptidir.

⚠️ **Yasal Uyarı:** Discord API'sine agresif istekler göndermek Discord Hizmet Şartları'na (ToS) aykırıdır. Hız sınırlarını (Rate Limit) aşarsanız botunuz veya IP adresiniz engellenebilir. Bu kod eğitim amaçlıdır ve tüm sorumluluk kullanıcıya aittir.

## Özellikler
- **Asenkron Yapı:** `aiohttp` kullanarak ping süresini minimuma indirir.
- **Otomatik Hız Sınırı Yönetimi:** Discord'dan 429 Rate Limit hatası alındığında ceza süresini otomatik okur ve spami durdurarak ban riskini azaltır.
- **Güvenli Konfigürasyon:** Hassas token ve sunucu verilerinizi ana kodun içine yazmak yerine `config.json` dosyasında tutar. Böylece kodu GitHub'da paylaşırken token'ınız ifşa olmaz.
- **Zaman Damgalı Loglama:** Başarı, hata ve deneme durumlarını saat ve tarih bilgisiyle birlikte terminale yansıtır.

## Kurulum ve Kullanım

### 1. Gereksinimleri Yükleyin
Sisteminizde Python 3.8+ kurulu olmalıdır. Gerekli asenkron HTTP kütüphanesini kurmak için:
```bash
pip install aiohttp
```
*(Ubuntu VDS kullanıcıları `pip install aiohttp --break-system-packages` komutunu kullanabilir).*

### 2. Ayarları Yapılandırın
Projeyi indirdikten sonra `config.json` dosyasını açın ve kendi bilgilerinizi girin:
```json
{
    "TOKEN": "BOT_TOKENINI_BURAYA_YAZ",
    "GUILD_ID": "SUNUCU_ID_BURAYA",
    "VANITY_CODE": "hedef_url",
    "DELAY": 1.0
}
```
- **DELAY:** Normal istekler arasındaki bekleme süresidir. Ban riskini düşürmek için 1.0 veya 0.5 kullanılması tavsiye edilir.

### 3. Çalıştırma

**Terminal Üzerinden (Standart):**
```bash
python3 sniper.py
```

**VDS Üzerinde 7/24 Kesintisiz (PM2 ile - Tavsiye Edilen):**
Scripti sunucuda arka planda kesintisiz çalıştırmak için PM2 kullanabilirsiniz.
```bash
pm2 start sniper.py --name "m0rte-sniper" --interpreter python3
pm2 logs m0rte-sniper
```
