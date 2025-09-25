import os
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio

TOKEN = os.getenv("BOT_TOKEN")  # El token lo pones en Render como variable de entorno
bot = Bot(TOKEN)

app = FastAPI()
application = Application.builder().token(TOKEN).build()

# --- Comando /start ---
async def start(update: Update, context):
    await update.message.reply_text("👋 Hola, soy tu bot para analizar imágenes.\nBOT HECHO POR LUIS 🤯")

application.add_handler(CommandHandler("start", start))

# --- Handler para fotos ---
async def handle_photo(update: Update, context):
    await update.message.reply_text("📷 Recibí tu foto. Estoy buscándola en internet...")

    # Aquí luego llamas a tu función de búsqueda Yandex/Bing
    # Ejemplo simplificado:
    await update.message.reply_text("✅ Resultado: (ejemplo de búsqueda)\nBOT HECHO POR LUIS 🤯")

application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# --- FastAPI endpoint para el webhook ---
@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

# --- Endpoint de prueba ---
@app.get("/")
async def home():
    return {"status": "Bot de Luis corriendo en Render 🤯"}