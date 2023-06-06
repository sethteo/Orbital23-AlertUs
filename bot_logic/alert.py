import time
from database.database import get_users, get_lowest_price
from bot.bot import alert
import asyncio

users = get_users()


while True:
    for current_user in users:
        price = get_lowest_price(current_user)
        if price:
            asyncio.run(alert(current_user["tele_id"], price))
            break
    time.sleep(10)

