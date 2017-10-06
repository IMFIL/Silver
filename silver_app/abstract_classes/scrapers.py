from abc import ABC, abstractmethod


class Scrapers(ABC):

    @abstractmethod
    def __init__(self, search_term):
        self.search_term = search_term

    @abstractmethod
    @property
    def products(self):
        pass

    @abstractmethod
    @property
    def html(self):
        pass
