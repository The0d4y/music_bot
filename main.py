import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import yt_dlp

# Obtener token desde variable de entorno
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No se encontró la variable de entorno BOT_TOKEN")

# Carpeta temporal para descargas
DOWNLOAD_DIR = "./downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Configuración de yt-dlp para mp3
YDL_OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'noplaylist': True,
}

# Función principal para manejar mensajes de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id

    # Mensaje de recepción
    await context.bot.send_message(chat_id=chat_id, text=f"Recibido: {user_text}\nBOT HECHO POR LUIS 🤯")

    # Descargar canción
    try:
        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(f"ytsearch1:{user_text}", download=True)
            filename = ydl.prepare_filename(info['entries'][0])
            mp3_file = os.path.splitext(filename)[0] + ".mp3"

        # Enviar mp3
        await context.bot.send_audio(chat_id=chat_id, audio=open(mp3_file, 'rb'),
                                     caption=f"Tu canción: {info['entries'][0]['title']}\nBOT HECHO POR LUIS 🤯")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Error al descargar: {e}\nBOT HECHO POR LUIS 🤯")

# Crear la aplicación
app = ApplicationBuilder().token(TOKEN).build()

# Agregar handler de mensajes de texto
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Ejecutar bot
if __name__ == '__main__':
    print("Bot corriendo...")
    app.run_polling()
