import requests
from bs4 import BeautifulSoup
from database.database import check_exist, create_new_user, add_item


# Scraping function that handles url from NTUC
def scrape_ntuc(url, username, tele_id):
    result = scrape_helper(url)
    price = result[0]
    item_name = result[1]
    add_to_db(url, price, item_name, username, tele_id)
    return price


# Scraping function that handles url from Cold Storage
def scrape_cs(url, username, tele_id):
    result = scrape_helper(url)
    price = result[0]
    item_name = result[1]
    add_to_db(url, price, item_name, username, tele_id)
    return price


# Helper method to facilitate user creation and user update
def add_to_db(url, price, item_name, username, tele_id):
    if check_exist(username):
        add_item(url, price, item_name, username)
    else:
        create_new_user(username, tele_id)
        add_item(url, price, item_name, username)


# Helper method to facilitate scraping and to reduce redundant code
def scrape_helper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if "fairprice" in url:
        price_element = soup.find("span", class_="sc-1bsd7ul-1 sc-13n2dsm-5 fQJDmX cpRMKK")
        item_element = soup.find("span", class_="sc-1bsd7ul-1 beGvbz")
        price = price_element.text.strip()
        item_name = item_element.text.strip()
        print(price, item_name)
        return [price, item_name]

    elif "coldstorage" in url:
        product = soup.find("div", id="product-info-content")
        price_data = product.find("div", class_="content_price")
        name_data = product.find("h1", class_="product-name main-heading")
        price = price_data.text.strip()
        item_name = name_data.text.strip()
        print(price, item_name)
        return [price, item_name]
