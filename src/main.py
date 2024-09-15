import requests
from bs4 import BeautifulSoup as bs
import sys
from crawl import *

    
if __name__ == "__main__":
    switch = sys.argv[1]
    if switch == "find_links":
        crawler = LinkCrawler(["paris", "berlin"])
        crawler.start(store=True)
    elif switch == "extract_pages":
        crawler = DataCrawler()
        crawler.start(store=True)
        
    