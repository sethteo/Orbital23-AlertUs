import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
import datetime

load_dotenv()

# Connecting to Mongo database
cluster = os.getenv('MONGO_CLUSTER')
client = MongoClient(cluster, tlsCAFile=certifi.where())
db = client.orbital
users = db.users


# Checks if user has any saved slots left
def check_user_slots(username):
    try:
        # Checks if user already exists, if exists, saves user as variable
        current_user = users.find_one({"name": username})
        # If user exists, returns true if their slots are > 0
        return current_user["slots"] > 0

    # When user does not exist, returns true by default
    except TypeError:
        return True


# Checks based on username if user exists in database, returns true if user exists
def check_exist(username):
    return users.count_documents({"name": username}) > 0


# Creates a new user with default parameters
def create_new_user(username, tele_id):
    new_user = {
        "tele_id": tele_id,
        "name": username,
        "items": [],
        "slots": 3,
    }
    users.insert_one(new_user)


# Adds an item to an existing user
def add_item(url, price, item_name, username):
    current_user = users.find_one({"name": username})
    # Creates a new item based on item schema
    new_item = {
        "itemUrl": url,
        "item_name": item_name,
        "initial_price": price,
        "price": [price],
        "date": [str(datetime.date.today())]
    }
    # Adds the newly created item into the user's item array
    users.update_one({"name": username}, {"$push": {"items": new_item}})
    # Decreases the user's number of slots by 1
    users.update_one({"name": username}, {"$set": {"slots": current_user["slots"] - 1}})


# Removes the item from an existing user
def remove_item(username, index):
    # Finds the user based on given username
    current_user = users.find_one({"name": username})
    # Finds the item based on given item index
    item_to_remove = ((current_user["items"])[index])["itemUrl"]
    # Increases the user's number of slots by 1
    users.update_one({"name": username}, {"$set": {"slots": current_user["slots"] + 1}})
    # Removes the selected item from the user's item array
    users.update_one({"name": username}, {"$pull": {"items": {"itemUrl": item_to_remove}}})


def list_item(username):
    # Returns an array containing all of the users saved items as Item objects
    current_user = users.find_one({"name": username})
    return current_user["items"]


def get_users():
    # Returns all users in database
    return users.find()


def append_price(url, name, price):
    # Updates the price array of an item based on the user's username and item's url
    users.update_one({"name": name, "items.itemUrl": url}, {"$push": {"items.$.price": price}})


def compare_price(user):
    # Retrieves item array from the current user
    items = user["items"]
    for item in items:
        # Obtain price array from every item
        prices = item["price"]
        # Converting item price from string to float
        initial_price = float(item['initial_price'].replace('$', ''))
        latest_price = float(prices[-1].replace('$', ''))
        if latest_price < initial_price:
            # Returns the latest price if latest price < initial price
            result = [prices[-1], item['item_name']]
            return result
        else:
            print('Initial price is the lowest price currently')
            return None


# Fetches an item based on given index and username, to be used in graph function
def get_item(username, index):
    # Retrieves current user based on username
    current_user = users.find_one({"name": username})

    # Retrieves price array from current user
    prices = current_user['items'][index - 1]['price']
    
    # Retrieves item name from current user's item
    item_name = current_user['items'][index - 1]['item_name']

    # Retrieves dates from current user's item
    dates = current_user['items'][index - 1]['date']
    updated_prices = []
    updated_dates = []
    for price in prices:
        # For every price in items's price array, convert from string to float
        updated_prices.append(float(price.replace('$', '')))
    for date in dates:
        # For every date in item's date array, convert from YYYY-MM-DD to DD-MM
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m")
        updated_dates.append(formatted_date)

    return [updated_prices, updated_dates, item_name]

def check_duplicate(url, username):
    current_user = users.find_one({"name": username})
    items = current_user['items']

    for item in items:
        if item['itemUrl'] == url:
            return True

    return False
