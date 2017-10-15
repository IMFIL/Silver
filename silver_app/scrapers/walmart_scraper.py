import json
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
from silver_app.abstract_classes.scrapers import Scrapers
import silver_app.models as db

#TODO implement Categories

class WalmartScraper(Scrapers):

    def __init__(self,search_term):
            self.search_term = search_term
            self.walmart_root_url = "https://www.walmart.com"
            self.walmart_main_page = "https://www.walmart.com/search/?query="
            self.walmart_search_page = '{}{}'.format(self.walmart_main_page, self.search_term.replace(" ","%20"))
            self.walmart_html_content = requests.get(self.walmart_search_page).text
            self.api_url = '{}{}'.format("http://api.walmartlabs.com/v1/search?apiKey=gyjh3k8nnt26xhrgybahqbfh&query=",self.search_term.replace(" ","%20"))


    def products(self,use_api=True):
        if use_api:
            try:
                api_request = requests.get(self.api_url)
                api_json_response = json.loads(json.dumps(api_request.json()))
                if api_json_response["totalResults"] < 1:
                    return []
            except Exception as exception:
                return self.products(False)

            item_from_request = api_json_response["items"]
            products_array = []

            for item in item_from_request:
                name = item["name"]
                price = item["salePrice"]
                image = item["thumbnailImage"]
                url = item["productUrl"]
                category = ""

                categoryInstance = db.Category(name=category)
                product = db.Product(name=name, category=categoryInstance, image=image)
                product_details = db.ProductDetails(product=product, amount=price, url=url, source="Walmart")
                products_array.append(product_details)

            return products_array

        else:
            walmart_soup = BeautifulSoup(self.walmart_html_content, "html.parser")
            results_div = walmart_soup.find_all("div","search-result-listview-items")

            if len(results_div) < 1:
                return []

            result_items = []

            if len(results_div) > 1:
                for div in results_div:
                    result_items.extend(div.find_all("div"))

            else:
                result_items = results_div[0]

            products_array = []

            for item in result_items:
                if not isinstance (item, NavigableString):
                    link = item.find("a","product-title-link")

                    if link is None:
                        continue

                    nameSpan = link.find("span")

                    if nameSpan is None:
                        continue

                    name = nameSpan.text
                    url = '{}{}'.format(self.walmart_root_url, link.get("href"))
                    item_content_div = item.find("div","tile-primary")

                    if item_content_div is None:
                        continue

                    priceSpan = item_content_div.find("span","Price-group")

                    if priceSpan is None:
                        continue

                    price = priceSpan.get("title")

                    imageDiv = item.find("div","search-result-productimage")

                    if imageDiv is None:
                        continue

                    imageContent = imageDiv.find("img","Tile-img")

                    if imageContent is None:
                        continue

                    image = imageContent.get("src")[2:]
                    category = ""

                    categoryInstance = db.Category(name=category)
                    product = db.Product(name=name, category=categoryInstance, image=image)
                    product_details = db.ProductDetails(product=product, amount=price, url=url, source="Walmart")
                    products_array.append(product_details)

            return products_array


    def html(self):
        return self.walmart_html_content
