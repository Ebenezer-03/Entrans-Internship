import os
from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "todo_db")
COLLECTION_NAME = "todos"

_client: Optional[MongoClient] = None

def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client

def get_collection() -> Collection:
    client = get_client()
    db = client[DB_NAME]
    return db[COLLECTION_NAME]
