from html_parser import *
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup as bs
from config import BASE_LINK, STORAGE_TYPE
import json
from parser import *
from storage import *

class CrawlerBase(ABC):
    
    def __init__(self):
        self.storage = self.__set_storage()
     
    @staticmethod   
    def __set_storage():
        if STORAGE_TYPE == 'mongo':
            return MongoStorage()
        return FileStorage()
        
    
    @abstractmethod
    def start(self, store=False):
        pass
    
    @abstractmethod
    def store(self, data, filename=None):
        pass
    
    @staticmethod
    def get(link):
        try:
            response = requests.get(link)
        except requests.HTTPError:
            return None
        return response
    
class LinkCrawler(CrawlerBase):
    
    def __init__(self, cities, link=BASE_LINK):
        self.cities = cities
        self.link = link
        super().__init__()
    
    def find_links(self, html_doc):
        soup = bs(html_doc, 'html.parser')
        return soup.find('ol').find_all('a')

    def crawl_cities(self, url):
        response = self.get(url)
        new_links = self.find_links(response.text)
        return new_links

    def start(self, store=False):
        total_links = list()
        for city in self.cities:
            links = self.crawl_cities(self.link.format(city))
            print(f'{city}: {len(links)}')
            total_links.extend(links)
        if store:
            self.store([{'url' : link.get('href'), 'flag' : False} for link in total_links])
        return total_links
            
    def store(self, data, *args):
        self.storage.store(data, 'advertisements_links')
            
    
    

class DataCrawler(CrawlerBase):
    
    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.parser = AdvertisementPageParser()
        
    def __load_links(self):
        return self.storage.load()
        
    def start(self, store=False):
        for link in self.links:
            response = self.get(link['url'])
            data = self.parser.parse(response.text)
            if store:
                self.store(data, data.get('post_id', 'sample'))
            self.storage.update_flag(link)    
            
    def store(self, data, filename):
        self.storage.store(data, 'advertisement_data')
            
            
            
            