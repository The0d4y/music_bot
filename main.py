import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")

# ------------------- Telegram Bot -------------------
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text("🎵 Hola! Mándame el nombre de una canción y te la descargo.\nBOT HECHO POR LUIS 🤯")

async def descargar_musica(update: Update, context):
    query = update.message.text
    await update.message.reply_text(f"⏳ Buscando: {query}")
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "song.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            filename = ydl.prepare_filename(info["entries"][0]).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        with open(filename, "rb") as song:
            await update.message.reply_audio(song)

        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# Registrar handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, descargar_musica))

# ------------------- Flask -------------------
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "OK", 200

# ------------------- Inicializar Bot -------------------
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.start())
    loop.run_forever()

# Lanzar el bot en un thread
threading.Thread(target=run_bot, daemon=True).start()

# ------------------- Main -------------------
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
