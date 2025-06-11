
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Например: https://your-railway-app.up.railway.app/webhook

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

@app.route("/")
def home():
    return "Bot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.run(application.process_update(update))
        return "ok", 200

async def start_bot():
    await application.initialize()
    await application.start()
    await bot.set_webhook(WEBHOOK_URL + "/webhook")
    print("Webhook set")

if __name__ == "__main__":
    asyncio.run(start_bot())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
