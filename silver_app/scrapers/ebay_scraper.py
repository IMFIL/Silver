import django
from django.conf import settings

settings.configure(DEBUG=True)
django.setup()

import json
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
from silver_app.abstract_classes.scrapers import Scrapers
import silver_app.models as db


class EbayScraper(Scrapers) :

    def __init__(self,search_term):
        Scrapers.__init__(self,search_term)
        self.ebay_main_page = "https://www.ebay.com/sch/"
        search_with_spaces = self.search_term.replace(" ","%20")
        self.ebay_search_page = self.ebay_main_page + search_with_spaces
        self.ebay_HTML_content = requests.get(self.ebay_search_page).text
        self.API_url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=FilipSla-Silver-PRD-e5d865283-eb1981df&REST-PAYLOAD&keywords="+search_with_spaces+"&RESPONSE-DATA-FORMAT=JSON"


    def products(self, useAPI = True):

        if useAPI:
            try:
                API_request = requests.get(self.API_url)
            except Exception as exception:
                return self.products(False)

            API_Json_response = json.loads(json.dumps(API_request.json()))
            item_from_request = API_Json_response["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
            products_array = []

            for item in item_from_request:
                name = item["title"]
                category = ""
                image = item["galleryURL"]

                categoryInstance = db.Category(name=category)
                product = db.Product(name=name,category=categoryInstance,image)

                price = item["sellingStatus"][0]["currentPrice"][0]["__value__"]

                product_detail = db.ProductDetails()
                products_array.append({"name":name, "category":category, "image":image, "price":price})


        else:
            ebay_soup = BeautifulSoup(self.ebay_HTML_content, "html.parser")
            results_ul = ebay_soup.find_all(id="ListViewInner")
            result_items = []

            if len(results_ul) > 1:
                for ul in results_ul:
                    result_items.extend(ul.find_all("li"))

            else:
                result_items = results_ul[0]

            products_array_objects = []

            for item in result_items:
                if not isinstance (item, NavigableString):
                    if item.find_all("h3",{"class":"lvtitle"}) == []:
                        continue
                    name = item.find_all("h3",{"class":"lvtitle"})[0].text.strip()
                    price = item.find_all("li", {"class":"lvprice"})[0].text.strip()
                    description = ""
                    category = ""
                    image = item.find_all("div",{"class":"lvpicinner"})[0].find_all("a")[0].get("href")

                    products_array_objects.append({"name":name,"price":price,"description":description, "category":category, "image":image})

                else:
                    continue



    def html(self):
        return self.ebay_HTML_content
