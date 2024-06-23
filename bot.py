from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, Dispatcher

TOKEN = "7456116559:AAGamCQDAr2Zj3PtvpWMcThyCEdZgcQB8a0"  # os.getenv("TELEGRAM_TOKEN")
FORBIDDEN_WORD = "https://t.me/hamster_kombat_bot/"  # os.getenv("HAMSTER_URL_BASE")
START_TEXT = "start text"  # os.getenv("HAMSTER_BAN_BOT_START_TEXT")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=START_TEXT)


def register_handlers(dispatcher):
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(MessageHandler(Filters.text, delete_messages_with_hamster, pass_user_data=True))


def delete_messages_with_hamster(update, context):
    message_text = update.message.text.lower()
    if FORBIDDEN_WORD in message_text:
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)


def update_bot(webhook_data):
    bot = Bot(token=TOKEN)
    update = Update.de_json(webhook_data.__dict__, bot)
    # updater = Updater(TOKEN, use_context=True)
    dp = Dispatcher(bot, None, workers=4)  # updater.dispatcher
    register_handlers(dp)
    dp.process_update(update)
