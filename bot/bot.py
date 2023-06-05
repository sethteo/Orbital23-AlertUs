import logging
import os
from dotenv import load_dotenv
from database.database import check_user_slots, remove_item, list_item
from bot_logic.scraper import scrape_ntuc, scrape_cs
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup

load_dotenv()

API_TOKEN = os.getenv('BOT_API')
WELCOME_TEXT = "Hello I am the AlertUs Bot and I can help you to track the prices of your items." \
               "\nPlease type /begin to continue or /help if you need help"
HELP_TEXT = "After entering or clicking /begin. \nChoose one of the options stated. " \
            "\nInsert the link of an item from the selected site" \
            "\nTo view all saved items please reply '/list' "\
            "\nTo remove an item please reply '/remove_' followed by the item number of the item you wish to remove"

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


# Helper method to obtain current user's username
def my_handler(message: types.Message):
    username = types.User.get_current().username
    tele_id = types.User.get_current().id
    return [username, tele_id]


# This handler will be called when user sends `/start` command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Prints out welcome text
    await message.reply(WELCOME_TEXT)


# This handler will be called when user sends `/help` command
@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    # Prints out help text
    await message.reply(HELP_TEXT)


# This handler will be called when user sends `/begin` command
@dp.message_handler(commands=['begin'])
async def begin(message: types.Message):
    # Gives user the inline keyboard options of "NTUC" or "Cold Storage"
    await message.reply("Please select an option", reply_markup=keyboard)


# This handler will be called when user sends `/list` command
@dp.message_handler(commands=['list'])
async def begin(message: types.Message):
    # Lists out all saved items of current user
    for item in list_item(my_handler(message)[0]):
        await message.reply(item["item_name"])


# This handler will be called when user sends /remove_"index"
@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['remove_([1-3]*)']))
async def remove_helper(message: types.Message, regexp_command):
    index = int(regexp_command.group(1))
    # Removes the item of the user based on the given index
    remove_item(my_handler(message)[0], (index - 1))
    await message.reply(f"Successfully removed item {index}")


# This handler is called after the "NTUC" or "Cold Storage" button is pressed after /begin command
# Is used to set the state to either "NTUC" or "Cold Storage"
@dp.callback_query_handler(text=["1", "2"])
async def function(call: types.callback_query):
    if call.data == "1":
        await Form.state_ntuc.set()
        await call.message.answer("Send me the link from NTUC :)")
    if call.data == "2":
        await Form.state_cs.set()
        await call.message.answer("Send me the link from Cold Storage :)")
    await call.answer()


# This handler is called if state is "NTUC"
@dp.message_handler(state=Form.state_ntuc)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    # Checks if user has sufficient slots
    if check_user_slots(my_handler(message)[0]):
        await message.reply(track_ntuc(message.text, my_handler(message)[0], my_handler(message)[1]))
    # Else prints out error message
    else:
        await message.answer("Sorry you do not have enough saved slots, please delete an item using /remove")


# This handler is called if state is "Cold Storage"
@dp.message_handler(state=Form.state_cs)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    # Checks if user has sufficient slots
    if check_user_slots(my_handler(message)[0]):
        await message.reply(track_cs(message.text, my_handler(message)[0], my_handler(message)[1]))
    # Else prints out error message
    else:
        await message.answer("Sorry you do not have enough saved slots, please delete an item using /remove")


# Helper method to be called if an item drops in price
async def alert(chat_id, price):
    await bot.send_message(chat_id=chat_id, text=f"Alert, your item has just dropped to {price}")


# Helper method to aid in tracking of NTUC items
def track_ntuc(url, username, tele_id):
    try:
        current_price = scrape_ntuc(url, username, tele_id)
        print(username)
        return f"The current price is {current_price}, I will notify you when it drops below it"
    except:
        return "Please select the option again and input a valid link"


# Helper method to aid in tracking of Cold Storage items
def track_cs(url, username, tele_id):
    try:
        current_price = scrape_cs(url, username, tele_id)
        print(username)
        return f"The current price is {current_price}, I will notify you when it drops below it"
    except:
        return "Please select the option again and input a valid link"


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

