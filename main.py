from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters
import os
import asyncio

TOKEN = os.getenv("7820783666:AAFO3ZupScBBiAuvi1IkSarGwkgR5mGxZNk")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT | filters.AUDIO | filters.VOICE, lambda u,c: asyncio.create_task(c.bot.send_message(chat_id=u.effective_chat.id, text="Received!")))

@app.route("/")
def home():
    return "Bot is running!", 200

@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return "ok", 200

async def start_bot():
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    await application.initialize()
    await application.start()
    print("Webhook set")

if __name__ == "__main__":
    asyncio.run(start_bot())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
