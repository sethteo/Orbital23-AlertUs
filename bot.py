import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '5660209243:AAFa6yf8AuxLLq2spli4NTjTLj03lGKA1_Q'
WELCOME_TEXT = "Hi I am the AlertUs Bot and can help you to track the prices of your items." \
               " Please select one of the options to continue"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


button_1 = InlineKeyboardButton(text="Shopee", callback_data="1")
button_2 = InlineKeyboardButton(text="Lazada", callback_data="2")
keyboard = InlineKeyboardMarkup().add(button_1, button_2)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply(WELCOME_TEXT)


@dp.message_handler(commands=['begin'])
async def begin(message: types.Message):
    await message.reply("Select an option", reply_markup=keyboard)


@dp.callback_query_handler(text=["1", "2"])
async def function(call: types.callback_query):
    if call.data == "1":
        await call.message.answer(foo1())
    if call.data == "2":
        await call.message.answer(foo2())
    await call.answer()


def foo1():
    return "Shopee"


def foo2():
    return "Lazada"


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
