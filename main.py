import discum
import os
from flask import Flask
from threading import Thread
import time

# --- Keep Alive Sunucu Kodu (OnRender için) ---
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
# .env dosyasından veya OnRender ortam değişkenlerinden token'ı alın
TOKEN = os.environ['TOKEN'] 
# Artık sunucu ID'sine ihtiyacımız yok. Kanal ID'si grup sohbetinin ID'si olacak.
GROUP_DM_ID = os.environ['VOICE_CHANNEL_ID'] 


bot = discum.Client(
    token=TOKEN,
    log=False # İsteğe bağlı: Daha temiz bir konsol için loglamayı kapatabilirsiniz
)

# Bu fonksiyon, sesli kanala (grup aramasına) katılmak için 
# gerekli olan opcode 4 payload'unu oluşturur ve gönderir.
def join_voice_group():
    print(f"[!] Grup aramasına ({GROUP_DM_ID}) katılma isteği hazırlanıyor...")
    # Bu, Discord'un ses durumu güncelleme komutudur (Opcode 4).
    payload = {
        "op": 4,
        "d": {
            # Grup aramaları için guild_id: None olmalıdır.
            "guild_id": None, 
            "channel_id": GROUP_DM_ID,
            "self_mute": True,  # Kendini sustur
            "self_deaf": True,   # Kendini sağırlaştır
        }
    }
    # Hazırladığımız komutu doğrudan gateway'e gönderiyoruz.
    bot.gateway.send(payload)
    print(f"[✓] Grup aramasına ({GROUP_DM_ID}) katılma isteği gönderildi.")


@bot.gateway.command
def on_ready(resp):
    # Bot 'READY' olayını aldığında, yani Discord'a başarıyla bağlandığında...
    if resp.event.ready:
        print(f"[✓] {bot.user['username']}#{bot.user['discriminator']} olarak Gateway'e bağlanıldı.")
        
        # Bazen anında istek göndermek başarısız olabilir.
        # Bağlantı tam olarak oturduktan sonra katılmak için küçük bir bekleme ekleyelim.
        time.sleep(3) 
        
        # Grup aramasına katılma fonksiyonunu çağır
        join_voice_group()

# Projeyi başlat
keep_alive()
print("[!] discum botu başlatılıyor...")
# auto_reconnect=True, botun bağlantısı koparsa yeniden bağlanmasını sağlar.
bot.gateway.run(auto_reconnect=True)
