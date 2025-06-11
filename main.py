from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

TOKEN = os.getenv("TOKEN") or "7820783666:AAFO3ZupScBBiAuvi1IkSarGwkgR5mGxZNk"

bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running!'

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "ok"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, я бот!")

application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start_command))

async def start_bot():
    await bot.set_webhook(url=f"https://{os.environ['RAILWAY_STATIC_URL']}/{TOKEN}")

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: asyncio.run(start_bot())).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
