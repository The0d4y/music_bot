import os
import yt_dlp
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Leer token desde variables de entorno
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # tu dominio de Render

# FastAPI app
app = FastAPI()

# Descargar música con yt-dlp
def download_music(url: str, filename: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎶 Envíame un link de YouTube y te lo descargo en MP3.\nBOT HECHO POR LUIS 🤯")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("⏳ Descargando música, espera un momento...\nBOT HECHO POR LUIS")

    filename = "song.mp3"
    try:
        download_music(url, filename)
        await update.message.reply_audio(audio=open(filename, "rb"), title="Tu canción 🎵")
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"❌ Error al descargar: {e}")

# Inicializar aplicación de Telegram
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Endpoint raíz
@app.get("/")
async def root():
    return {"status": "Bot de Luis funcionando en Render 🤯"}

# Endpoint webhook
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}

# Configuración de webhook al arrancar
@app.on_event("startup")
async def set_webhook():
    if WEBHOOK_URL:
        await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
