import discum
import os
from flask import Flask
from threading import Thread

# --- Keep Alive Sunucu Kodu ---
app = Flask('')

@app.route('/')
def home():
    return "Bot çalışıyor."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --- Sunucu Kodu Bitişi ---


# --- discum Bot Kodu ---
TOKEN = os.environ['TOKEN']
# ID'leri discum'a string olarak vermek genellikle daha güvenlidir.
GUILD_ID = os.environ['GUILD_ID']
VOICE_CHANNEL_ID = os.environ['VOICE_CHANNEL_ID']


bot = discum.Client(
    token=TOKEN,
    log=True
)

# Bu fonksiyon, sesli kanala katılmak için gerekli olan
# opcode 4 payload'unu (ağ geçidi komutunu) oluşturur ve gönderir.
# discum arka planda bu komutu işleyip ses websocket'ini ve
# kalp atışlarını yönetecektir.
def join_voice():
    # Bu, Discord'un ses durumu güncelleme komutudur (Opcode 4).
    payload = {
        "op": 4,
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": VOICE_CHANNEL_ID,
            "self_mute": True,  # Kendini sustur
            "self_deaf": True,   # Kendini sağırlaştır
        }
    }
    # Hazırladığımız komutu doğrudan gateway'e gönderiyoruz.
    bot.gateway.send(payload)
    print(f"[✓] Ses kanalına ({VOICE_CHANNEL_ID}) katılma isteği doğrudan gönderildi.")


@bot.gateway.command
def on_ready(resp):
    # Bot 'READY' olayını aldığında, yani Discord'a başarıyla bağlandığında...
    if resp.event.ready:
        print("[✓] Gateway'e bağlanıldı ve READY olayı alındı.")
        # Ses kanalına katılma fonksiyonunu çağır
        join_voice()

# Projeyi başlat
keep_alive()
print("[!] discum botu başlatılıyor...")
# auto_reconnect=True, botun bağlantısı koparsa yeniden bağlanmasını sağlar.
bot.gateway.run(auto_reconnect=True)
