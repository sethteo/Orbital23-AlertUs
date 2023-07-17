import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
import datetime

load_dotenv()

cluster = os.getenv('MONGO_CLUSTER')
client = MongoClient(cluster, tlsCAFile=certifi.where())
db = client.orbital
users = db.users


# Checks if user has any saved slots left
def check_user_slots(username):
    try:
        current_user = users.find_one({"name": username})
        return current_user["slots"] > 0
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
    new_item = {
        "itemUrl": url,
        "item_name": item_name,
        "initial_price": price,
        "price": [price],
        "date": [str(datetime.date.today())]
    }
    users.update_one({"name": username}, {"$push": {"items": new_item}})
    users.update_one({"name": username}, {"$set": {"slots": current_user["slots"] - 1}})


# Removes the item from an existing user
def remove_item(username, index):
    current_user = users.find_one({"name": username})
    item_to_remove = ((current_user["items"])[index])["itemUrl"]
    print(item_to_remove)
    users.update_one({"name": username}, {"$set": {"slots": current_user["slots"] + 1}})
    users.update_one({"name": username}, {"$pull": {"items": {"itemUrl": item_to_remove}}})


def list_item(username):
    current_user = users.find_one({"name": username})
    return current_user["items"]


def get_users():
    return users.find()


def append_price(url, name, price):
    users.update_one({"name": name, "items.itemUrl": url}, {"$push": {"items.$.price": price}})


def compare_price(user):
    items = user["items"]
    for item in items:
        prices = item["price"]
        initial_price = float(item['initial_price'].replace('$', ''))
        latest_price = float(prices[-1].replace('$', ''))
        if latest_price < initial_price:
            result = [prices[-1], item['item_name']]
            return result
        else:
            print('Initial price is the lowest price currently')
            return None


def get_item(username, index):
    current_user = users.find_one({"name": username})
    prices = current_user['items'][index - 1]['price']
    item_name = current_user['items'][index - 1]['item_name']
    updated_prices = []
    for price in prices:
        updated_prices.append(float(price.replace('$', '')))
    return [updated_prices, item_name]
