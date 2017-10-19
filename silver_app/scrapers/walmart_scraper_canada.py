import json

import django
from django.conf import settings
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
from silver_app.abstract_classes.scrapers import Scrapers
import silver_app.models as db

#TODO implement Categories

class WalmartScraper(Scrapers):

    def __init__(self,search_term):
            self.search_term = search_term
            self.walmart_root_url = "https://www.walmart.ca"
            self.walmart_main_page = "https://www.walmart.ca/search/"
            self.walmart_search_page = '{}{}'.format(self.walmart_main_page, self.search_term.replace(" ","%20"))
            self.walmart_html_content = requests.get(self.walmart_search_page).text


    def products(self):
        pass

    def html(self):
        return self.walmart_html_content
