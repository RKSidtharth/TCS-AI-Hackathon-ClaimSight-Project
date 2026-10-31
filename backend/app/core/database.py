"""
CLAIMSIGHT AI - MongoDB Connection and Collection Accessors
"""

import pymongo
from app.core.config import settings

class Database:
    client: pymongo.MongoClient = None
    db = None

    @classmethod
    def connect(cls):
        if cls.client is None:
            cls.client = pymongo.MongoClient(settings.MONGODB_URI)
            cls.db = cls.client[settings.MONGODB_DB_NAME]
            print(f"[*] Connected to MongoDB: {settings.MONGODB_DB_NAME}")

    @classmethod
    def get_db(cls):
        if cls.db is None:
            cls.connect()
        return cls.db

    @classmethod
    def close(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None
            print("[*] MongoDB connection closed.")

def get_database():
    return Database.get_db()

