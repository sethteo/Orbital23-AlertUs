from pymongo import MongoClient
import certifi

cluster = "mongodb+srv://sethteo:7mkyhyUofIqFaeoP@orbitalalertus.ibhfals.mongodb.net/?retryWrites=true&w=majority"
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
def create_new_user(username):
    new_user = {
        "name": username,
        "itemUrl": "",
        "price": [],
        "slots": 1
    }
    users.insert_one(new_user)


# Adds an item to an existing user
def add_item(url, price, username):
    current_user = users.find_one({"name": username})
    users.update_one({"name": username}, {"$set": {"itemUrl": url}})
    users.update_one({"name": username}, {"$push": {"price": price}})
    users.update_one({"name": username}, {"$set": {"slots": current_user["slots"] - 1}})


# Removes the item from an existing user
'''Can consider doing an index deletion'''


def remove_item(username):
    current_user = users.find_one({"name": username})
    users.update_one({"name": username}, {"$set": {"itemUrl": ""}})
    users.update_one({"name": username}, {"$set": {"slots": current_user["slots"] + 1}})






test_user = {
    "name": "mightbehr",
    "itemUrl": "url",
    "price": [1, 2, 3],
    "slots": 1
}
