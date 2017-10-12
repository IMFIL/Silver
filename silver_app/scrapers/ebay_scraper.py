import json
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
from silver_app.abstract_classes.scrapers import Scrapers
import silver_app.models as db


class EbayScraper(Scrapers) :

    def __init__(self,search_term):
        self.search_term = search_term
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
            ebay_soup = BeautifulSoup(self.ebay_HTML_content, "html.parser")
            results_ul = ebay_soup.find_all(id="ListViewInner")
            result_items = []

            if len(results_ul) > 1:
                for ul in results_ul:
                    result_items.extend(ul.find_all("li"))

            else:
                result_items = results_ul[0]

            products_array = []

            for item in result_items:
                if not isinstance (item, NavigableString):
                    if item.find_all("h3",{"class":"lvtitle"}) == []:
                        continue
                    title =item.find_all("h3",{"class":"lvtitle"})[0]
                    name = title.text.strip()
                    image = item.find_all("div",{"class":"lvpicinner"})[0].find_all("img")[0].get("src")
                    category = ""

                    categoryInstance = db.Category(name=category)
                    product = db.Product(name=name, category=categoryInstance, image=image)

                    url =  title.find("a").get("href")
                    price = item.find_all("li", {"class":"lvprice"})[0].text.strip()

                    product_details = db.ProductDetails(product=product, amount=price, url=url, source="Ebay")

                    products_array.append(product_details)

                else:
                    continue

            return products_array

    def html(self):
        return self.ebay_HTML_content
