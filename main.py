import os
from typing import Optional

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI

from bot import update_bot

app = FastAPI()


class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]


@app.get("/")
def index():
    return {"message": "bot works"}


@app.post("/webhook")
def webhook(webhook_data: TelegramWebhook):
    update_bot(webhook_data)
    # updater.start_polling()
    # updater.idle()
    return {"message": "ok"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
