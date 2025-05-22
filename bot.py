import os
import requests
from telegram.ext import ApplicationBuilder, CommandHandler

ESP_IP = "http://192.168.1.100"  # ESP32 IP adresinizle değiştirin

def pixel_to_distance(x):
    table = {
        718: 30, 617: 40, 536: 50, 473: 60, 435: 70, 395: 80, 362: 90,
        335: 100, 312: 110, 290: 120, 273: 130, 256: 140, 243: 150,
        230: 160, 220: 170, 210: 180, 200: 190, 191: 200, 183: 210,
        178: 220, 171: 230, 165: 240, 159: 250, 154: 260, 149: 270,
        146: 280, 140: 290, 136: 300, 132: 310, 129: 320, 125: 330,
        123: 340, 120: 350, 117: 360, 114: 370, 111: 380, 109: 390,
        106: 400, 104: 410, 102: 420, 100: 430, 98: 440, 96: 450,
        94: 460, 92: 470, 91: 480, 89: 490, 88: 500, 86: 510, 84: 520,
        83: 530, 82: 540, 81: 550, 80: 560, 79: 570, 77: 580, 76: 590,
        74: 600, 73: 610, 72: 620, 72: 630, 71: 640, 70: 650, 69: 660
    }
    nearest = min(table.keys(), key=lambda k: abs(k - x))
    return table[nearest]

async def bul(update, context):
    try:
        r = requests.get(f"{ESP_IP}/coords", timeout=5)
        if r.status_code == 200:
            data = r.json()
            x = data.get("x")
            if x == -1:
                await update.message.reply_text("Lazer noktası bulunamadı.")
                return
            cm = pixel_to_distance(x)
            await update.message.reply_text(f"Lazer mesafesi yaklaşık: {cm} cm (x={x})")
        else:
            await update.message.reply_text("ESP32 cevap vermedi.")
    except Exception as e:
        await update.message.reply_text(f"Hata: {str(e)}")

async def start(update, context):
    await update.message.reply_text("Hoş geldin! /bul komutunu kullanarak lazer mesafesini öğrenebilirsin.")

def main():
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bul", bul))
    app.run_polling()

if __name__ == "__main__":
    main()
