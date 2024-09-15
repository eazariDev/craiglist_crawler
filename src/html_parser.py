from bs4 import BeautifulSoup as bs
import re

class AdvertisementPageParser:
    
    
    def __init__(self):
        self.soup = None
        
    @property
    def title(self):
        title_tag = self.soup.find('span', attrs={'id': 'titletextonly'})
        if title_tag:
            return title_tag.text
        return None

    @property
    def price(self):
        price_tag = self.soup.find('span', attrs={'class': 'price'})
        if price_tag:
            return price_tag.text
        return None
    
    @property
    def body(self):
        body_tag = self.soup.select_one('#postingbody')
        if body_tag:
            return body_tag.text
        return None
    
    @property
    def post_id(self):
        selector = 'body > section > section > section > div.postinginfos > p:nth-child(1)'
        post_id_tag = self.soup.select_one(selector)
        if post_id_tag:
           # return post_id_tag.text.replace('Id publi: ', '')
            return ''.join(re.findall(r'\d+', post_id_tag.text))
        return None
    
    @property
    def created_time(self):
        selector = 'body > section > section > section > div.postinginfos > p:nth-child(2) > time'
        time = self.soup.select_one(selector)
        if time:
            return time.attrs['datetime']
        return None
    
    @property
    def modified_time(self):
        selector = 'body > section > section > section > div.postinginfos > p:nth-child(3) > time'
        time = self.soup.select_one(selector)
        if time:
            return time.attrs['datetime']
        return None
    
        
    def parse(self, html_data):
        self.soup = bs(html_data, 'html.parser')
        data = dict( title=self.title,
                    price = self.price,
                    body = self.body,
                    post_id=self.post_id,
                    created_time=self.created_time,
                    modified_time=self.modified_time
        )

        
        return data