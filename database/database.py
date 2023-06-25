import os
from dotenv import load_dotenv
from pymongo import MongoClient
import pymongo
import certifi

load_dotenv()

cluster = os.getenv('MONGO_CLUSTER')
client = pymongo.MongoClient(cluster, tlsCAFile=certifi.where())
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
        "price": [price],
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

# code to update price
# url = "https://www.fairprice.com.sg/product/fairprice-adult-diaper-pants-m-10-per-pack-13180730"
# users.update_one({"name":"mightbehr", "items.itemUrl": url}, {"$push": {"items.$.price": "$12.80"}})


def get_lowest_price(user):
    items = user["items"]
    for item in items:
        prices = item["price"]
        initial = float(prices[0].replace('$', ''))
        latest_price = float(prices[-1].replace('$', ''))
        if latest_price < initial:
            result = [prices[-1], item['item_name']]
            return result
        else:
            return None

#users.update_one({"name":"mightbehr", "items.itemUrl": url}, {"$push": {"items.$.price": "$5.80"}})

# test = users.find_one({"name": "mightbehr"})
# get_lowest_price(test)

# print(test)

