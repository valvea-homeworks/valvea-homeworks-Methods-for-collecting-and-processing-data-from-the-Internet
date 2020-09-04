from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class Manage_db:
    def __init__(self):
        self.client = MongoClient('127.0.0.1', 27017)

    def get_db(self, name):
        return self.client[name]

    def get_collection(self,db,name):
        return db[name]

    def update_collection(self,collection_,values):
        for value in values:
            try:
                collection_.insert_one(value)
                print('Значение успешно добавлено,',f'коллекция {collection_.name}')
            except DuplicateKeyError:
                print('Такое значение уже есть')





