import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

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
        "itemUrl": "",
        "item_name": "",
        "price": [],
        "slots": 1
    }
    users.insert_one(new_user)


# Adds an item to an existing user
def add_item(url, price, item_name, username):
    current_user = users.find_one({"name": username})
    users.update_one({"name": username}, {"$set": {"itemUrl": url}})
    users.update_one({"name": username}, {"$set": {"item_name": item_name}})
    users.update_one({"name": username}, {"$push": {"price": price}})
    users.update_one({"name": username}, {"$set": {"slots": current_user["slots"] - 1}})


# Removes the item from an existing user
def remove_item(username, index):
    current_user = users.find_one({"name": username})
    users.update_one({"name": username}, {"$set": {"itemUrl": ""}})
    users.update_one({"name": username}, {"$set": {"slots": current_user["slots"] + 1}})


def list_item(username):
    current_user = users.find_one({"name": username})
    return current_user["item_name"]


def get_users():
    return users.find()

