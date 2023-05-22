import requests
from bs4 import BeautifulSoup
from database import check_exist, create_new_user, add_item


# Scraping function that handles url from NTUC
def scrape_ntuc(url, username):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    price_element = soup.find("span", class_="sc-1bsd7ul-1 sc-13n2dsm-5 fQJDmX cpRMKK")
    item_element = soup.find("span", class_="sc-1bsd7ul-1 beGvbz")
    price = price_element.text.strip()
    item_name = item_element.text.strip()
    add_to_db(url, price, item_name, username)

    print(price, item_name)
    return price


# Scraping function that handles url from Cold Storage
def scrape_cs(url, username):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    product = soup.find("div", class_="product-detail")
    price_data = product.find("div", class_="price_now price_normal f-green disc")
    name_data = product.find("h1", class_="product-name main-heading")
    price = price_data.text.strip()
    item_name = name_data.text.strip()
    add_to_db(url, price, item_name, username)

    print(price, item_name)
    return price


# Helper method to facilitate user creation and user update
def add_to_db(url, price, item_name, username):
    if check_exist(username):
        add_item(url, price, item_name, username)
    else:
        create_new_user(username)
        add_item(url, price, item_name, username)


scrape_ntuc("https://www.fairprice.com.sg/product/pasar-prepacked-carrots-500g-13000321", "hr")
scrape_cs("https://coldstorage.com.sg/cabernet-sauvignon-5007180", "hr")
