import json
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
from silver_app.abstract_classes.scrapers import Scrapers
import silver_app.models as db

#TODO implement Categories

class EbayScraper(Scrapers) :

    def __init__(self,search_term):
        self.search_term = search_term
        self.ebay_main_page = "https://www.ebay.ca/sch/"
        self.ebay_search_page = '{}{}'.format(self.ebay_main_page, self.search_term.replace(" ","%20"))
        self.ebay_html_content = requests.get(self.ebay_search_page).text
        self.api_url = '{}{}'.format("http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=FilipSla-Silver-PRD-e5d865283-eb1981df&REST-PAYLOAD&RESPONSE-DATA-FORMAT=JSON&GLOBAL-ID=2&keywords=",self.search_term.replace(" ","%20"))


    def products(self, use_api = True):

        if use_api:
            try:
                api_request = requests.get(self.api_url)
                api_json_response = json.loads(json.dumps(api_request.json()))
                if int(api_json_response["findItemsByKeywordsResponse"][0]["searchResult"][0]["@count"]) < 1:
                    return []
            except Exception as exception:
                return self.products(False)

            item_from_request = api_json_response["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
            products_array = []

            for item in item_from_request:
                name = item["title"][0]
                category = ""
                image = item["galleryURL"][0]

                categoryInstance = db.Category(name=category)
                product = db.Product(name=name, category=categoryInstance, image=image)

                price = item["sellingStatus"][0]["currentPrice"][0]["__value__"]
                url = item["viewItemURL"][0]
                product_details = db.ProductDetails(product=product, amount=price, url=url, source="Ebay")
                products_array.append(product_details)

            return products_array
        else:
            ebay_soup = BeautifulSoup(self.ebay_html_content, "html.parser")
            results_ul = ebay_soup.find_all(id="ListViewInner")

            if len(results_ul) < 1:
                return []

            result_items = []

            if len(results_ul) > 1:
                for ul in results_ul:
                    result_items.extend(ul.find_all("li"))

            else:
                result_items = results_ul[0]

            products_array = []

            for item in result_items:
                if not isinstance (item, NavigableString):
                    if item.find("h3", "lvtitle") == None:
                        continue
                    title =item.find("h3", "lvtitle")
                    name = title.text.strip()
                    image = item.find("div", "lvpicinner").find("img").get("src")
                    category = ""

                    categoryInstance = db.Category(name=category)
                    product = db.Product(name=name, category=categoryInstance, image=image)

                    url =  title.find("a").get("href")
                    price = item.find("li", "lvprice").text.strip()

                    product_details = db.ProductDetails(product=product, amount=price, url=url, source="Ebay")

                    products_array.append(product_details)


            return products_array

    def html(self):
        return self.ebay_html_content
