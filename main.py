import os
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = os.getenv("TELEGRAM_TOKEN")
FORBIDDEN_WORD = os.getenv("HAMSTER_URL_BASE")


def delete_messages_with_hamster(update, context):
    message_text = update.message.text.lower()
    if FORBIDDEN_WORD in message_text:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)


if __name__ == '__main__':
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, delete_messages_with_hamster, pass_user_data=True))
    updater.start_polling()
    updater.idle()
