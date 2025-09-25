import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import yt_dlp as youtube_dl
from tempfile import NamedTemporaryFile

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Debes configurar la variable de entorno BOT_TOKEN")

# Función para descargar audio mp3 desde yt-dlp
def download_audio(query: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # Si query es URL usa directamente, si no usa búsqueda
        if query.startswith("http"):
            info = ydl.extract_info(query, download=True)
        else:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)['entries'][0]

        filename = ydl.prepare_filename(info)
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        return mp3_filename, info.get('title', 'Canción')

# Función que maneja los mensajes de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id, f"Recibido tu pedido: '{user_text}'… BOT HECHO POR LUIS 🤯")

    try:
        mp3_file, title = download_audio(user_text)
        with open(mp3_file, 'rb') as f:
            await context.bot.send_audio(chat_id, audio=f, title=title)
        await context.bot.send_message(chat_id, f"Tu canción '{title}' ha sido enviada 🎵 BOT HECHO POR LUIS 🤯")
    except Exception as e:
        logging.error(f"Error al descargar: {e}")
        await context.bot.send_message(chat_id, f"Error al descargar: {e} BOT HECHO POR LUIS 🤯")

# Crear la aplicación de Telegram
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Configurar webhook en Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logging.info(f"Bot corriendo en puerto {port}…")

    # URL de tu app en Render
    WEBHOOK_URL = f"https://music-bot-xs5m.onrender.com/webhook"

    # Inicializar webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="webhook",
        webhook_url=WEBHOOK_URL
    )
