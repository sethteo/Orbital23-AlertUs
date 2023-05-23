import time
from database import check_price
from bot import alert
import asyncio


while True:
    if check_price():
        user_id = check_price()[0]
        price = check_price()[1]
        asyncio.run(alert(user_id, price))
    time.sleep(3600)




