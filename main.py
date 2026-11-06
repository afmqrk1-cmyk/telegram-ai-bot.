

import os
import asyncio
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from google import genai

logging.basicConfig(level=logging.INFO)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я AFM AI 🤖\n"
        "Я работаю на Google Gemini. Задавай вопросы!"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=update.message.text
        )

        answer = response.text or "Не удалось получить ответ."

        await update.message.reply_text(answer)

    except Exception:
        logging.exception("Gemini error")
        await update.message.reply_text(
            "Произошла ошибка. Попробуй позже."
        )

def main():
    app = Application.builder().token(
        os.getenv("BOT_TOKEN")
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    app.run_polling()

if __name__ == "__main__":
    main()

