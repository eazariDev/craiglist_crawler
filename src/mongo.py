from pymongo import MongoClient

#to avoid multiple connection, we use singleton pattern on only have on connection to db(one isntance)
class MongoDatabase:
    
    instance = None
    
    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(*args, **kwargs)
        return cls.instance
    
    def __init__(self):
        self.client = MongoClient()
        self.database = self.client['crawler_db']