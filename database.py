from pymongo import MongoClient
import certifi


cluster = "mongodb+srv://sethteo:7mkyhyUofIqFaeoP@orbitalalertus.ibhfals.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster, tlsCAFile=certifi.where())
db = client.orbital


user = {
    "name": "mightbehr",
    "item": "url",
    "price": [1, 2, 3],
    "slots": 1
}
users = db.users


# Checks if user has any saved slots left
def check_user(username):
    current_user = users.find_one({"name": username})
    return current_user["slots"] > 0


def add_item(url, price):
    return 0


def remove_item(url):
    return 0
