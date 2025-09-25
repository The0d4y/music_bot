import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
YT_COOKIES = os.environ.get("YT_COOKIES")  # Ruta al archivo cookies.txt

ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
}

if YT_COOKIES:
    ydl_opts["cookiefile"] = YT_COOKIES

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Envía el nombre de la canción y te la entregaré en mp3.\nBOT HECHO POR LUIS 🤯"
    )

async def download_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"Buscando y descargando: {query}\nBOT HECHO POR LUIS 🤯")
    
    # yt-dlp usa búsqueda de YouTube si le pasas "ytsearch1:query"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            file_path = ydl.prepare_filename(info['entries'][0])
            mp3_path = file_path.rsplit(".", 1)[0] + ".mp3"
        
        with open(mp3_path, "rb") as f:
            await update.message.reply_audio(f, filename=mp3_path.split("/")[-1])
        
        await update.message.reply_text(f"¡Listo! 🎵\nBOT HECHO POR LUIS 🤯")
    except Exception as e:
        await update.message.reply_text(f"Error al descargar: {e}\nBOT HECHO POR LUIS 🤯")

# Construir aplicación
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_song))

# Webhook (Render env)
PORT = int(os.environ.get("PORT", "8443"))
URL = os.environ.get("APP_URL")  # p.ej: https://music-bot-xs5m.onrender.com

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{URL}/{BOT_TOKEN}"
    )
