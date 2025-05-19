from pymongo import MongoClient
import os

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        mongo_uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client.get_default_database()

    def close(self):
        if self.client:
            self.client.close()

    def get_collection(self, collection_name):
        if self.db:
            return self.db[collection_name]
        raise Exception("Database not connected")