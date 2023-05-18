import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Our bot token
BOT_TOKEN = "5660209243:AAFa6yf8AuxLLq2spli4NTjTLj03lGKA1_Q"
WELCOME_TEXT = "Hi I am the AlertUs Bot and can help you to track the prices of your items." \
               " Please select one of the options to continue"
ERROR_TEXT = "Sorry, I did not understand that. Please try again."

# Setting up our logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# Functions to handle each command
# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_TEXT)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_TEXT)


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ERROR_TEXT)


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    #application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(unknown_handler)

    application.run_polling()


