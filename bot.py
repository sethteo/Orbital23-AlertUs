import logging
from scraper import scrape_ntuc, scrape_cs

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


API_TOKEN = '5660209243:AAFa6yf8AuxLLq2spli4NTjTLj03lGKA1_Q'
WELCOME_TEXT = "Hello I am the AlertUs Bot and I can help you to track the prices of your items." \
               "\nPlease type /begin to continue or /help if you need help"
HELP_TEXT = "After entering or clicking /begin. \nChoose one of the options stated. " \
            "\nInsert the link of an item from the selected site"

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


button_1 = InlineKeyboardButton(text="NTUC", callback_data="1")
button_2 = InlineKeyboardButton(text="Cold Storage", callback_data="2")
keyboard = InlineKeyboardMarkup().add(button_1, button_2)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # This handler will be called when user sends `/start` command
    await message.reply(WELCOME_TEXT)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    # This handler will be called when user sends `/help` command
    await message.reply(HELP_TEXT)


@dp.message_handler(commands=['begin'])
async def begin(message: types.Message):
    # This handler will be called when user sends `/begin` command
    await message.reply("Please select an option", reply_markup=keyboard)


@dp.callback_query_handler(text=["1", "2"])
async def function(call: types.callback_query):
    if call.data == "1":
        await call.message.answer(foo1())
    if call.data == "2":
        await call.message.answer(foo2())
    await call.answer()


def foo1():
    return scrape_ntuc("https://www.fairprice.com.sg/product/aw-s-market-fresh-malaysian-pork-big-spare-ribs-300-g-90110551")


def foo2():
    return scrape_cs("https://coldstorage.com.sg/meadows-roasted-cashews-150g-5071784")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
