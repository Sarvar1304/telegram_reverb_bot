import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
FFMPEG_PATH = "ffmpeg"

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.audio.get_file() if update.message.audio else await update.message.voice.get_file()
    input_path = "input.ogg"
    output_path = "output.mp3"

    await file.download_to_drive(input_path)

    command = [
        FFMPEG_PATH,
        "-i", input_path,
        "-af", "aecho=0.8:0.88:60:0.4",
        "-codec:a", "libmp3lame",
        "-y",
        output_path
    ]
    subprocess.run(command, check=True)

    with open(output_path, 'rb') as audio:
        await update.message.reply_audio(
            audio=audio,
            filename="reverb.mp3",
            title="Reverb FX"
        )

    os.remove(input_path)
    os.remove(output_path)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
app.run_polling()
