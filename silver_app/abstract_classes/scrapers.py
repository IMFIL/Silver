from abc import ABC, abstractmethod


class Scrapers(ABC):

    @abstractmethod
    def products(self):
        pass

    @abstractmethod
    def html(self):
        pass
