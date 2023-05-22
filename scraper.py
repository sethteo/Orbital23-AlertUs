import requests
from bs4 import BeautifulSoup
from database import check_exist, create_new_user, add_item


# Scraping function that handles url from NTUC
def scrape_ntuc(url, username):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    price_element = soup.find("span", class_="sc-1bsd7ul-1 sc-13n2dsm-5 fQJDmX cpRMKK")
    price = price_element.text.strip()
    add_to_db(url, price, username)

    print(price)
    return price


# Scraping function that handles url from Cold Storage
def scrape_cs(url, username):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    price_element = soup.find("div", class_="product-detail")
    price_data = price_element.find("div", class_="price_now price_normal f-green disc")
    price = price_data.text.strip()
    add_to_db(url, price, username)

    print(price)
    return price


# Helper method to facilitate user creation and user update
def add_to_db(url, price, username):
    if check_exist(username):
        add_item(url, price, username)
    else:
        create_new_user(username)
        add_item(url, price, username)

