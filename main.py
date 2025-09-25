import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp
import asyncio

TOKEN = os.getenv("BOT_TOKEN")

# Creamos la aplicación de Telegram
application = Application.builder().token(TOKEN).build()

# ------------------- Handlers -------------------
async def start(update: Update, context):
    await update.message.reply_text("🎵 Hola! Mándame el nombre o una parte de una canción y te la descargo.\nBOT HECHO POR LUIS 🤯")

async def descargar_musica(update: Update, context):
    query = update.message.text
    await update.message.reply_text(f"⏳ Buscando\n espere un momento por favor..\nBOT HECHO POR LUIS🤯: {query}")
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

@app.before_first_request
def init_bot():
    """Inicializar y arrancar el bot cuando Flask arranca"""
    loop = asyncio.get_event_loop()
    loop.create_task(application.initialize())
    loop.create_task(application.start())

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "OK", 200

# ------------------- Main -------------------
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
