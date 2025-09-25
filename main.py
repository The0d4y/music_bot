from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp
import os

BOT_TOKEN = "TU_BOT_TOKEN_AQUI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Envía el nombre de la canción o enlace de YouTube y te la devolveré en MP3.\nBOT HECHO POR LUIS 🤯"
    )

async def download_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id

    # Mensaje de recibido
    await update.message.reply_text(f"Recibido: {text}\nComenzando descarga... BOT HECHO POR LUIS 🤯")

    # Configuración de yt-dlp para MP3
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        # Si es un enlace, úsalo directamente; si no, búsqueda en YouTube
        query = text if text.startswith("http") else f"ytsearch1:{text}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info_dict)
            # Cambia extensión a .mp3
            filename = os.path.splitext(filename)[0] + ".mp3"

        # Enviar archivo MP3
        with open(filename, 'rb') as f:
            await context.bot.send_document(chat_id, document=f, filename=os.path.basename(filename))

        # Mensaje de entrega
        await update.message.reply_text(f"¡Descarga completada! BOT HECHO POR LUIS 🤯")

        # Borrar archivo
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"Error al descargar: {str(e)} BOT HECHO POR LUIS 🤯")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_song))

    print("Bot corriendo...")
    app.run_polling()
