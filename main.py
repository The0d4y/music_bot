import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import asyncio
import pathlib

# Variables de entorno en Render
BOT_TOKEN = os.environ.get("BOT_TOKEN")
YT_COOKIES = os.environ.get("YT_COOKIES")  # opcional
PORT = int(os.environ.get("PORT", 5000))
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")  # Render asigna esta URL automáticamente

# Opciones de yt-dlp para solo mp3
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'nocheckcertificate': True,
}

if YT_COOKIES:
    ydl_opts['cookiefile'] = YT_COOKIES

# Función para manejar mensajes de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id

    await context.bot.send_message(chat_id=chat_id, text=f"Recibido: {text}… BOT HECHO POR LUIS 🤯")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{text}", download=True)
            filename = ydl.prepare_filename(info['entries'][0])
            # Convertir extensión a .mp3 si es necesario
            if not filename.endswith(".mp3"):
                filename = pathlib.Path(filename).with_suffix(".mp3")
        
        # Enviar el mp3 al usuario
        with open(filename, 'rb') as f:
            await context.bot.send_audio(chat_id=chat_id, audio=f, title=text)

        await context.bot.send_message(chat_id=chat_id, text=f"Tu canción se ha enviado ✅ BOT HECHO POR LUIS 🤯")
        
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Error al descargar: {e} BOT HECHO POR LUIS 🤯")
    
    finally:
        # Limpiar archivos mp3 descargados
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except:
            pass

# Crear la aplicación
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Ejecutar webhook en Render
if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="/webhook",
        webhook_url=f"{RENDER_URL}/webhook"
                                      )
