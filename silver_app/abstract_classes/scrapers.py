from abc import ABC, abstractmethod


class Scrapers(ABC):

    @abstractmethod
    def __init__(self, url):
        self.url = url

    @abstractmethod
    @property
    def products(self):
        if self.products == None:
            pass
        else:
            pass

    @property
    def scraper_url(self):
        return self.url

    @abstractmethod
    def getHTML(self):
        pass
