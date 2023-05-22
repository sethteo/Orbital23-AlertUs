import requests
from bs4 import BeautifulSoup
from database import check_exist, create_new_user, add_item


# Scraping function that handles url from NTUC
def scrape_ntuc(url, username):
    result = scrape_helper(url, "ntuc")
    price = result[0]
    item_name = result[1]
    add_to_db(url, price, item_name, username)
    return price


# Scraping function that handles url from Cold Storage
def scrape_cs(url, username):
    result = scrape_helper(url, "cs")
    price = result[0]
    item_name = result[1]
    add_to_db(url, price, item_name, username)
    return price


# Helper method to facilitate user creation and user update
def add_to_db(url, price, item_name, username):
    if check_exist(username):
        add_item(url, price, item_name, username)
    else:
        create_new_user(username)
        add_item(url, price, item_name, username)


# Helper method to facilitate scraping and to reduce redundant code
def scrape_helper(url, store_type):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if store_type == "ntuc":
        price_element = soup.find("span", class_="sc-1bsd7ul-1 sc-13n2dsm-5 fQJDmX cpRMKK")
        item_element = soup.find("span", class_="sc-1bsd7ul-1 beGvbz")
        price = price_element.text.strip()
        item_name = item_element.text.strip()
        print(price, item_name)
        return [price, item_name]

    elif store_type == "cs":
        product = soup.find("div", class_="product-detail")
        price_data = product.find("div", class_="price_now price_normal f-green disc")
        name_data = product.find("h1", class_="product-name main-heading")
        price = price_data.text.strip()
        item_name = name_data.text.strip()
        print(price, item_name)
        return [price, item_name]
