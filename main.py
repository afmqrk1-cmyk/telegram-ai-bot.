
import os
import asyncio
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

ai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я ИИ-помощник на базе GPT. Спрашивай что угодно!"
    )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = await asyncio.to_thread(
            ai.responses.create,
            model="gpt-6-astra",
            instructions="Ты дружелюбный русскоязычный помощник.",
            input=update.message.text
        )
        await update.message.reply_text(response.output_text)
    except Exception:
        await update.message.reply_text(
            "Не удалось получить ответ. Попробуй позже."
        )

def main():
    app = Application.builder().token(
        os.environ["BOT_TOKEN"]
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
    )
    app.run_polling()

if __name__ == "__main__":
    main()
