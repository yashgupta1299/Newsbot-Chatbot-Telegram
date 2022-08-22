import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update, ReplyKeyboardMarkup
from utils import get_reply, fetch_news, topics_keyboard

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# telegram bot token
TOKEN = "###############################"

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello!"

@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    update = Update.de_json(request.get_json(), bot)
    # process update
    dp.process_update(update)
    return "ok"


def start(update, context):
    #     """callback function for /start handler"""
    print(update)
    author = update.message.from_user.first_name
    reply = "Hi! {}".format(author)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply)

def _help(update, context):
#     """callback function for /help handler"""
    help_text = "I will do your help!"
    context.bot.send_message(chat_id=update.message.chat_id, text=help_text)


def news(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Choose a category", 
        reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))

# def echo_text(update, context):
# #     """callback function for text message handler"""
#     reply = update.message.text
#     context.bot.send_message(chat_id=update.message.chat_id, text=reply)

def reply_text(update, context):
    """callback function for text message handler"""
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            context.bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(update, context):
#     """callback function for sticker message handler"""

    context.bot.send_sticker(chat_id=update.message.chat_id, sticker=update.message.sticker.file_id)

def error(update, context):
#     """callback function for error handler"""
    logger.error("Update '%s' caused '%s' error", context, context.error)

bot = Bot(TOKEN)

try:
    bot.set_webhook("##############################" + TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)

if __name__ == "__main__":
    app.run(port=8443)
    