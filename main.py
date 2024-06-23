from contextlib import asynccontextmanager
from typing import Optional
import uvicorn
from fastapi.openapi.models import Response
from fastapi import FastAPI, Request
from http import HTTPStatus
import os
from telegram import Update
from telegram.ext import MessageHandler, Application, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")
FORBIDDEN_WORD = os.getenv("HAMSTER_URL_BASE")
WEBHOOK_BASE = os.getenv("WEBHOOK_BASE")


async def delete_messages_with_hamster(update, context):
    print("new message")
    message_text = update.message.text.lower()
    if FORBIDDEN_WORD in message_text:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)


telegram_bot = (Application.builder()
                .updater(None)
                .token(TOKEN)
                .read_timeout(7)
                .get_updates_read_timeout(42)
                .build())
telegram_bot.add_handler(MessageHandler(filters.TEXT, delete_messages_with_hamster))


@asynccontextmanager
async def lifespan(_: FastAPI):
    await telegram_bot.bot.setWebhook(f"https://api.telegram.org/bot{TOKEN}/"
                                      f"setWebhook?url={WEBHOOK_BASE}")
    async with telegram_bot:
        await telegram_bot.start()
        yield
        await telegram_bot.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"message": "bot works"}


@app.post("/")
async def process_update(request: Request):
    request_json = await request.json()
    update = Update.de_json(request_json, telegram_bot.bot)
    if not telegram_bot._initialized:
        await telegram_bot.initialize()
    await telegram_bot.process_update(update)
    return {"message": "ok"}  # Response(status_code=HTTPStatus.OK)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
