import time
from database import get_users
from bot import alert
from scraper import scrape_helper
import asyncio

users = get_users()


def check_price():
    for user in users:
        prices = user["price"]
        initial = float(prices[0].replace('$', ''))
        for curr_price in prices:
            price_in_float = float(curr_price.replace('$', ''))
            if price_in_float < initial:
                return [user["tele_id"], curr_price]


while True:
    user = check_price()
    user_id = user[0]
    price = user[1]
    asyncio.run(alert(user_id, price))
    time.sleep(60)
