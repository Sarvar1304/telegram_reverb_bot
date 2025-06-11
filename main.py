import os
import subprocess
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "7820783666:AAFO3ZupScBBiAuvi1IkSarGwkgR5mGxZNk"
FFMPEG_PATH = "attached_assets/ffmpeg-7.0.2-amd64-static/ffmpeg"

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.audio.get_file(
    ) if update.message.audio else await update.message.voice.get_file()
    input_path = "input.ogg"
    output_path = "output.mp3"

    await file.download_to_drive(input_path)

    command = [
        FFMPEG_PATH, "-i", input_path, "-af", "aecho=0.8:0.88:60:0.4",
        "-codec:a", "libmp3lame", "-y", output_path
    ]
    subprocess.run(command, check=True)

    with open(output_path, 'rb') as audio:
        await update.message.reply_audio(audio=audio,
                                         filename="reverb.mp3",
                                         title="Reverb FX")

    os.remove(input_path)
    os.remove(output_path)


application.add_handler(
    MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"


if __name__ == "__main__":
    import asyncio

    async def start():
        await application.initialize()
        await application.start()
        await bot.set_webhook(
            url=
            f"https://{os.environ['REPL_SLUG']}.{os.environ['REPL_OWNER']}.repl.co/{TOKEN}"
        )
        app.run(host="0.0.0.0", port=8080)

    asyncio.run(start())
