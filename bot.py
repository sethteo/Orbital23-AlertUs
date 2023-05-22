import logging
from database import check_user_slots
from scraper import scrape_ntuc, scrape_cs
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

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
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    state_ntuc = State()
    state_cs = State()


button_1 = InlineKeyboardButton(text="NTUC", callback_data="1")
button_2 = InlineKeyboardButton(text="Cold Storage", callback_data="2")
keyboard = InlineKeyboardMarkup().add(button_1, button_2)


# helper method to obtain current user's username
def my_handler(message: types.Message):
    user = types.User.get_current()
    return user.username


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
        await Form.state_ntuc.set()
        await call.message.answer("Send me the link from NTUC :)")
    if call.data == "2":
        await Form.state_cs.set()
        await call.message.answer("Send me the link from Cold Storage :)")
    await call.answer()


@dp.message_handler(state=Form.state_ntuc)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    # Checks if user has sufficient slots
    if check_user_slots(my_handler(message)):
        await message.reply(track_ntuc(message.text, my_handler(message)))
    # Else prints out error message
    else:
        await message.answer("Sorry you do not have enough saved slots, please delete an item using /remove")


@dp.message_handler(state=Form.state_cs)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    # Checks if user has sufficient slots
    if check_user_slots(my_handler(message)):
        await message.reply(track_cs(message.text, my_handler(message)))
    # Else prints out error message
    else:
        await message.answer("Sorry you do not have enough saved slots, please delete an item using /remove")


def track_ntuc(url, username):
    try:
        current_price = scrape_ntuc(url, username)
        print(username)
        return f"The current price is {current_price}, I will notify you when it drops below it"
    except:
        return "Please select the option again and input a valid link"


def track_cs(url, username):
    try:
        current_price = scrape_cs(url, username)
        print(username)
        return f"The current price is {current_price}, I will notify you when it drops below it"
    except:
        return "Please select the option again and input a valid link"


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
