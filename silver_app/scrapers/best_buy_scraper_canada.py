import json
from bs4 import BeautifulSoup
from lxml import html
import requests
from silver_app.abstract_classes.scrapers import Scrapers
import silver_app.models as db

#TODO implement Categories

class BestBuyScraper(Scrapers) :

    def __init__(self,search_term):
        self.search_term = search_term
        self.best_buy_home_url = "https://www.bestbuy.ca"
        self.best_buy_search_url = "https://www.bestbuy.ca/en-CA/Search/SearchResults.aspx?query="
        self.search_query_url = '{}{}'.format(self.best_buy_search_url, self.search_term)
        self.response = requests.get(self.search_query_url).content

    def products(self, use_api = True):

        products = []

        if use_api:
            search_with_spaces = self.search_term.replace(" ","%20")
            # Later on when we have the affilate partnership, use "linkShareAffiliateUrl"
            API_url = "https://api.bestbuy.com/v1/products(search={})?format=json&show=name,salePrice,image,url&apiKey=OAQAbTMEDbYABRCoKpNMRcGI".format(search_with_spaces)
            
            try: 
                API_response = requests.get(API_url) 
                products_json = API_response.json()["products"]
            
            except Exception as exception:
                return self.products(False)

            for product in products_json:
                product_name = product["name"]
                product_price = product["salePrice"]
                product_image = product["image"]
                product_url = product["url"]
                product_category = ""
                
                categoryInstance = db.Category(name=product_category)
                product = db.Product(name=product_name, category=categoryInstance, image=product_image)
                product_details = db.ProductDetails(product=product, amount=product_price, url=product_url, source="BestBuy")

                products.append(product_details)


        else:
            soup = BeautifulSoup(self.response, 'lxml')
            products_html = soup.find_all(class_="listing-item")

            if not products_html:
                print("Products list empty...")
                return self.products(False)

            for product in products_html:
                product_name = product.find(class_="prod-info").find(class_="prod-title").text
                product_price = product.find(class_="prod-info").find(class_="prodprice").find("span").text
                product_image = product.find(class_="prod-image").find("img")["src"]
                product_url = '{}{}'.format(self.best_buy_home_url, product.find(class_="prod-info").find(class_="prod-title").find("a")["href"])
                product_category = ""

                categoryInstance = db.Category(name=product_category)
                product = db.Product(name=product_name, category=categoryInstance, image=product_image)
                product_details = db.ProductDetails(product=product, amount=product_price, url=product_url, source="BestBuy")

                products.append(product_details)

        return products

    def html(self):
        return self.response

# query = input("Enter search query: ")
# scraper = BestBuyScraper(query)
# scraper.products(False)
