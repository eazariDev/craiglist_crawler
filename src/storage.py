from abc import ABC, abstractmethod
import json
from mongo import *

class StorageAbstract(ABC):
    
    @abstractmethod
    def store(self, data, *args):
        pass

    @abstractmethod
    def load(self):
        pass

class MongoStorage(StorageAbstract):
    
    def __init__(self):
        self.mongo = MongoDatabase()
        
        
    def store(self, data, collection, *args):
        collection = getattr(self.mongo.database, collection)
        if len(data) > 1 and isinstance(data, list):
            collection.insert_many(data)
        else:
            collection.insert_one(data)
            
    def load(self):
        return self.mongo.database.advertisements_links.find({'flag': False})

    def update_flag(self, data):
        self.mongo.database.advertisements_links.find_one_and_update({'_id' : data['_id']},{'$set': {'flag' : True}})

class FileStorage(StorageAbstract):
    
    def store(self, data, filename, *args):
        if isinstance(data, dict):
            filename = filename + '-' + data['post_id']
        with open(f'data/adv/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
        print(f'data/adv/{filename}.json')
        
    def load(self):
        with open('data/adv/advertisements_links.json', 'r') as f:
            links = json.loads(f.read())
        return links