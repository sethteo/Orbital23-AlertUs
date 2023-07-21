from database.database import get_users, append_price, compare_price
from bot_logic.scraper import scrape_helper
from bot import alert
import asyncio
import os
from apscheduler.schedulers.blocking import BlockingScheduler

users = get_users()


# Loops through every item of every user and fetches the latest price of that item
# and updates the price array of that item
def update_price():
    for user in users:
        items = user['items']
        for item in items:
            currentItemUrl = item['itemUrl']
            new_price = scrape_helper(currentItemUrl)[0]
            print(new_price)
            append_price(currentItemUrl, user['name'], new_price)


def check_price():
    for user in users:
        if compare_price(user):
            chat_id = user['tele_id']
            price = compare_price(user)[0]
            item_name = compare_price(user)[1]
            asyncio.run(alert(chat_id, price, item_name))


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(update_price, 'interval', days=1)
    scheduler.add_job(check_price, 'interval', hours=12)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
