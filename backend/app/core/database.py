"""
CLAIMSIGHT AI - MongoDB Connection and Collection Accessors
Supports live MongoDB (local & Atlas) with zero-config in-memory fallback for Vercel Serverless.
"""

import os
import sys
import pymongo
from app.core.config import settings

class Database:
    client = None
    db = None

    @classmethod
    def connect(cls):
        if cls.client is not None and cls.db is not None:
            return cls.db

        # 1. Attempt connection to configured MongoDB URI (Atlas or Local)
        try:
            client = pymongo.MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=1500)
            client.admin.command('ping')
            cls.client = client
            cls.db = client[settings.MONGODB_DB_NAME]
            print(f"[*] Connected to Live MongoDB: {settings.MONGODB_DB_NAME}")
            return cls.db
        except Exception as err:
            print(f"[!] Live MongoDB not available ({err}). Activating Serverless In-Memory Data Store...")

        # 2. Resilient Serverless Fallback via mongomock
        try:
            import mongomock
            cls.client = mongomock.MongoClient()
            cls.db = cls.client[settings.MONGODB_DB_NAME]

            # Seed in-memory database with synthetic claims and data
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)

            try:
                from database.seed.seed_data import seed_database
                seed_database(client=cls.client, db_name=settings.MONGODB_DB_NAME)
                print("[*] CLAIMSIGHT AI Serverless In-Memory Data Store seeded successfully.")
            except Exception as s_err:
                print(f"[!] Warning: Seed fallback partial error: {s_err}")

            return cls.db
        except Exception as mock_err:
            print(f"[!] Fatal: Could not initialize fallback mock DB: {mock_err}")
            return None

    @classmethod
    def get_db(cls):
        if cls.db is None:
            cls.connect()
        return cls.db

    @classmethod
    def close(cls):
        if cls.client:
            try:
                cls.client.close()
            except Exception:
                pass
            cls.client = None
            cls.db = None
            print("[*] Database connection closed.")

def get_database():
    return Database.get_db()

