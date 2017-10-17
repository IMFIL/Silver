import json
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
from silver_app.abstract_classes.scrapers import Scrapers
import silver_app.models as db

#TODO implement Categories

class TargetScraper(Scrapers):

    def __init__(self,search_term):
            self.target_root_url = "https://intl.target.com"
            self.search_term = search_term
            self.api_url = '{}{}'.format("https://redsky.target.com/v1/plp/search?count=24&keyword=",self.search_term.replace(" ","+"))


    def products(self):
        try:
            api_request = requests.get(self.api_url)
            api_json_response = json.loads(json.dumps(api_request.json()))
        except Exception as exception:
            return []

        item_from_request = api_json_response["search_response"]["items"]["Item"]
        products_array = []

        for item in item_from_request:
            name = item["title"]
            price = item["offer_price"]["price"]
            image = '{}{}'.format(item["images"][0]["base_url"], item["images"][0]["primary"])
            url = '{}{}'.format(self.target_root_url, item["url"])
            category = ""

            categoryInstance = db.Category(name=category)
            product = db.Product(name=name, category=categoryInstance, image=image)
            product_details = db.ProductDetails(product=product, amount=price, url=url, source="Target")
            products_array.append(product_details)

        return products_array

    def html(self):
        return ""
