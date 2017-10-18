import json
from bs4 import BeautifulSoup
from lxml import html
import requests
from silver_app.abstract_classes.scrapers import scrapers
import silver_app.models as db

#TODO implement Categories
#TODO API key was REVOKED... I don't think they give it out publicly...

class BestBuyScraper(Scrapers) :

    def __init__(self,search_term):
        self.search_term = search_term
        self.best_buy_home_url = "https://www.bestbuy.ca"
        self.best_buy_search_url = "https://www.bestbuy.ca/en-CA/Search/SearchResults.aspx?query="
        self.search_query_url = self.best_buy_search_url + self.search_term

    def products(self, use_api = False):

        products = []

        if usingAPI:
            search_with_spaces = self.search_term.replace(" ","%20")
            API_url = "https://api.bestbuy.com/v1/products(search=" + search_with_spaces + ")?format=json&show=name,salePrice&apiKey=L2ZspyGow9YLq8lfxdgQ4bBw"
            API_response = requests.get(API_url) 

            products_json = API_response.json()["products"]

            for product in products_json:
                product_name = product["name"]
                product_price = product["salePrice"]
                product_image = ""
                product_url = ""
                product_category = ""
                
                categoryInstance = db.Category(name=product_category)
                product = db.Product(name=product_name, category=categoryInstance, image=product_image)
                product_details = db.ProductDetails(product=product, amount=product_price, url=product_url, source="BestBuy")

                products.append(product_details)


        else:
            response = requests.get(self.search_query_url)
            soup = BeautifulSoup(response.content, 'lxml')

            products_html = soup.find_all(class_="listing-item")

            if not products_html:
                print("Products list empty...")

            for product in products_html:
                product_name = product.find(class_="prod-info").find(class_="prod-title").text
                product_price = product.find(class_="prod-info").find(class_="prodprice").find("span").text
                product_image = product.find(class_="prod-image").find("img")["src"]
                product_url = self.best_buy_home_url + product.find(class_="prod-info").find(class_="prod-title").find("a")["href"]
                product_category = ""

                categoryInstance = db.Category(name=product_category)
                product = db.Product(name=product_name, category=categoryInstance, image=product_image)
                product_details = db.ProductDetails(product=product, amount=product_price, url=product_url, source="BestBuy")

                products.append(product_details)

        return products

    def html(self):
        return self.best_buy_search_page

query = input("Enter search query: ")
scraper = BestBuyScraper(query)
scraper.products(False)
