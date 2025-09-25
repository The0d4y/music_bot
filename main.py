from flask import Flask, request
import asyncio
from telegram import Update, InputFile, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp
import os

TOKEN = os.getenv("BOT_TOKEN")  # Tu token en Variables de Entorno
bot = Bot(token=TOKEN)
app = Flask(__name__)

# ---------------- Handlers ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola! Soy tu bot de música.\n"
        "📥 Envía el enlace de YouTube o TikTok para descargar audio.\n"
        "BOT HECHO POR LUIS 🤯"
    )

async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text(f"🔍 Recibido: {url}\nBOT HECHO POR LUIS 🤯")

    output_file = "audio.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(output_file, "rb") as f:
            await update.message.reply_audio(
                audio=InputFile(f),
                caption=f"✅ Aquí tienes tu música!\nBOT HECHO POR LUIS 🤯"
            )
        os.remove(output_file)

    except Exception as e:
        await update.message.reply_text(f"❌ Error al descargar: {e}\nBOT HECHO POR LUIS 🤯")

# ---------------- Telegram Webhook ---------------- #

async def telegram_webhook():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, downloader))
    await application.initialize()
    return application

application = asyncio.run(telegram_webhook())

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "OK"

@app.route("/")
def index():
    return "Bot de música activo! BOT HECHO POR LUIS 🤯"

# ---------------- Run Flask ---------------- #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
