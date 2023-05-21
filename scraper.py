import requests
from bs4 import BeautifulSoup


def scrape_ntuc(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    price_element = soup.find("span", class_="sc-1bsd7ul-1 sc-13n2dsm-5 fQJDmX cpRMKK")
    price = price_element.text.strip()
    print(price)
    return price


def scrape_cs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    price_element = soup.find("div", class_="product-detail")
    price_data = price_element.find("div", class_="price_now price_normal f-green disc")
    price = price_data.text.strip()
    print(price)
    return price


def scrape_ss(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    price_element = soup.find("div", class_="product-price-tag")

    return price_element

# scrape_ntuc("https://www.fairprice.com.sg/product/aw-s-market-fresh-malaysian-pork-big-spare-ribs-300-g-90110551")
# scrape_cs("https://coldstorage.com.sg/meadows-roasted-cashews-150g-5071784")
scrape_ss("https://shengsiong.com.sg/product/kelloggs-soy-protein-granola-honey-almond-220-gram")
