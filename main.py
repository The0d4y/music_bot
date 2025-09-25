# main.py
import os
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
import yt_dlp

TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text(
        "¡Hola! Envía el nombre de la canción o enlace y te la descargaré en MP3. BOT HECHO POR LUIS 🤯"
    )

async def download_music(update: Update, context):
    query = update.message.text
    await update.message.reply_text(f"Recibido: {query}… BOT HECHO POR LUIS 🤯")

    # Creamos un directorio temporal para la descarga
    with tempfile.TemporaryDirectory() as tmpdirname:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{tmpdirname}/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                filename = os.path.join(tmpdirname, f"{info['title']}.mp3")

            # Enviar el archivo al usuario
            await update.message.reply_document(
                document=open(filename, 'rb'),
                filename=os.path.basename(filename),
                caption=f"Aquí tienes tu música: {os.path.basename(filename)}… BOT HECHO POR LUIS 🤯"
            )

        except Exception as e:
            await update.message.reply_text(f"Error al descargar: {e}… BOT HECHO POR LUIS 🤯")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_music))

if __name__ == "__main__":
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"https://music-bot-xs5m.onrender.com/webhook"
            )
