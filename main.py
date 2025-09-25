import os
import yt_dlp
import socket
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ----- Dummy port para Render -----
def open_dummy_port():
    try:
        port = int(os.environ.get("PORT", 5000))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", port))
        sock.listen(1)
        print(f"Dummy port abierto en {port} para Render")
        while True:
            conn, _ = sock.accept()
            conn.close()
    except Exception:
        pass  # cualquier error lo ignoramos, no rompe el bot

# Ejecutar en un hilo separado, sin bloquear el bot
threading.Thread(target=open_dummy_port, daemon=True).start()

# Ruta al archivo cookies.txt en la raíz
COOKIE_PATH = "cookies.txt"

# Función de inicio / bienvenida
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Envía el nombre de una canción y te la enviaré en MP3.\nBOT HECHO POR LUIS 🤯"
    )

# Función que maneja los mensajes de texto (nombres de canciones)
async def descargar_musica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    chat_id = update.message.chat_id

    # Mensaje de recepción
    await update.message.reply_text(f"Recibido: {query}\nBuscando la canción... BOT HECHO POR LUIS 🤯")

    # Configuración de yt-dlp
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        "outtmpl": f"{query}.%(ext)s",
        "cookiefile": COOKIE_PATH
    }

    try:
        # Buscar y descargar usando ytsearch
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            filename = ydl.prepare_filename(info)
            mp3_file = os.path.splitext(filename)[0] + ".mp3"

        # Enviar el archivo MP3 al usuario
        await context.bot.send_audio(chat_id=chat_id, audio=open(mp3_file, "rb"))
        await update.message.reply_text("Canción entregada con éxito! BOT HECHO POR LUIS 🤯")

        # Eliminar el archivo descargado para no acumular
        os.remove(mp3_file)

    except Exception as e:
        await update.message.reply_text(f"Error al descargar: {e} BOT HECHO POR LUIS 🤯")

# Crear la aplicación
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Asegúrate de tener BOT_TOKEN en variables de entorno
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Registrar handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, descargar_musica))

# Iniciar bot
app.run_polling()
