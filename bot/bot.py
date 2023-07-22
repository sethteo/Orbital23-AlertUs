import logging
import os
import io
import matplotlib.pyplot as plt
from PIL import Image
from dotenv import load_dotenv
from database.database import check_user_slots, remove_item, list_item, get_item
from bot_logic.scraper import scrape_ntuc, scrape_cs
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup

load_dotenv()

API_TOKEN = os.getenv("BOT_API")
WELCOME_TEXT = (
    "Hello I am the AlertUs Bot and I can help you to track the prices of your items."
    "\nPlease type /begin to continue or /help if you need help"
)
HELP_TEXT = (
    "Basic tier members are given 3 item slots"
    "\n- After entering or clicking /begin. \n- Choose one of the options stated. "
    "\n- Insert the link of an item from the selected site"
)
LIST_TEXT = "\nTo view all saved items please reply '/list' "
REMOVE_TEXT = "\nTo remove an item please reply '/remove_' followed by the item number of the item you wish to remove"
GRAPH_TEXT = "\nTo view a price against time graph of your item, please reply '/graph_' followed by the item number of the item you wish to plot"

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Set states to enable the use of NTUC and Cold Storage buttons
class Form(StatesGroup):
    state_ntuc = State()
    state_cs = State()


button_1 = InlineKeyboardButton(text="NTUC", callback_data="1")
button_2 = InlineKeyboardButton(text="Cold Storage", callback_data="2")
keyboard = InlineKeyboardMarkup().add(button_1, button_2)


# Helper method to obtain current user's username and telegram id
def my_handler(message: types.Message):
    username = types.User.get_current().username
    tele_id = types.User.get_current().id
    return [username, tele_id]


# This handler will be called when user sends `/start` command
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    # Prints out welcome text
    await message.reply(WELCOME_TEXT)


# This handler will be called when user sends `/help` command
@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    # Saves all instruction images as variables to be sent
    help_photo = open('images/help.png', "rb")
    list_photo = open('images/list.png', "rb")
    remove_photo = open('images/remove.png', "rb")
    graph_photo = open('images/graph.png', "rb")
    await bot.send_photo(chat_id=message.chat.id, photo=help_photo)
    await message.reply(HELP_TEXT)
    await bot.send_photo(chat_id=message.chat.id, photo=list_photo)
    await message.reply(LIST_TEXT)
    await bot.send_photo(chat_id=message.chat.id, photo=remove_photo)
    await message.reply(REMOVE_TEXT)
    await bot.send_photo(chat_id=message.chat.id, photo=graph_photo)
    await message.reply(GRAPH_TEXT)


# This handler will be called when user sends `/begin` command
@dp.message_handler(commands=["begin"])
async def begin(message: types.Message):
    # Gives user the inline keyboard options of "NTUC" or "Cold Storage"
    await message.reply("Please select an option", reply_markup=keyboard)


# This handler will be called when user sends `/list` command
@dp.message_handler(commands=["list"])
async def begin(message: types.Message):
    # Lists out all saved items of current user using user's username
    items = list_item(my_handler(message)[0])

    
    if items:
        # If user currently has saved items, loops through each item and sends item name
        for i in range(1, len(items) + 1):
            item = items[i - 1]
            await message.reply(f"{i}. {item['item_name']}")
    else:
        # Else prints error message
        await message.reply("You do not have any saved items")


# This handler will be called when user sends /remove_"index"
@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=["remove_([1-3]*)"]))
async def remove_helper(message: types.Message, regexp_command):
    index = int(regexp_command.group(1))
    # Removes the item of the user based on the given index
    try:
        remove_item(my_handler(message)[0], (index - 1))
        await message.reply(f"Successfully removed item {index}")
    # Catches index out of bounds error, e.g. when user inputs an index not in range of array
    except IndexError:
        await message.reply(f"There is no such item of index {index}")


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
    url = message.text
    username = my_handler(message)[0]
    tele_id = my_handler(message)[1]
    
    # Checks if given url is a duplicate
    if check_duplicate(url, my_handler(message)[0]):
        await message.answer("You have already saved this item, please try again.")
    # Checks if user has sufficient slots
    elif check_user_slots(my_handler(message)[0]):
        await message.reply(track_ntuc(url, username, tele_id))
    # Else prints out error message
    else:
        await message.answer("Sorry you do not have enough saved slots, please delete an item using /remove")


# This handler is called if state is "Cold Storage"
@dp.message_handler(state=Form.state_cs)
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    url = message.text
    username = my_handler(message)[0]
    tele_id = my_handler(message)[1]

    # Checks if given url is a duplicate
    if check_duplicate(url, username):
        await message.answer("You have already saved this item, please try again.")
    # Checks if user has sufficient slots
    elif check_user_slots(my_handler(message)[0]):
        await message.reply(track_cs(message.text, username, tele_id))
    # Else prints out error message
    else:
        await message.answer("Sorry you do not have enough saved slots, please delete an item using /remove")


# Helper method to be called if an item drops in price
# Takes in user's telegram id, new price of item and name of item
async def alert(telegram_id, price, item_name):
    # Sends a message to the given user
    await bot.send_message(
        chat_id=telegram_id,
        text=f"Alert, your item: {item_name} has just dropped to {price}",
    )


# Helper method to aid in tracking of NTUC items
def track_ntuc(url, username, tele_id):
    # Tries to scrape the given string by the user
    try:
        current_price = scrape_ntuc(url, username, tele_id)
        print(username)
        return f"The current price is {current_price}, I will notify you when it drops below it"
    # Except when the link is invalid
    except:
        return "Please select the option again and input a valid link"


# Helper method to aid in tracking of Cold Storage items
def track_cs(url, username, tele_id):
    # Tries to scrape the given string by the user
    try:
        current_price = scrape_cs(url, username, tele_id)
        print(username)
        return f"The current price is {current_price}, I will notify you when it drops below it"
    # Except when the link is invalid
    except:
        return "Please select the option again and input a valid link"


# This handler will be called when user sends /graph_"index"
@dp.message_handler(regexp_commands=['graph_([1-3]*)'])
async def send_welcome(message: types.Message, regexp_command):
    # Tries to plot a graph based on the user's item's index
    try:
        index = int(regexp_command.group(1))
        username = types.User.get_current().username

        # Fetches the item from the database using the username and index
        data = get_item(username, index)

        # get_item returns an array of [price, date, itemName]
        price_data = data[0]
        date_data = data[1]
        item_name = data[2]

        # Plotting the graph
        plt.plot(price_data, "o-")

        # Setting of axis labels
        plt.xlabel('Date')
        plt.ylabel('Price')

        # Setting graph name
        plt.title(f'{item_name}')

        # Create an in-memory buffer so as to not store the image in native directory
        buffer = io.BytesIO()  

        # Sets points
        plt.xticks(range(len(price_data)), date_data)

        # Save the plot to the buffer
        plt.savefig(buffer, format='png') 

        # Move the buffer's cursor to the beginning
        buffer.seek(0) 

        # Obtaining image from buffer
        image = Image.open(buffer)
        photo = buffer.getvalue()

        # Closing the current buffer
        buffer.close()

        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        await message.reply(f"This is the graph for item: {item_name}")
    # Except when the given index is out of the user's item array
    except IndexError:
        await message.answer(f"Sorry you do not have a saved item with index: {index}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
