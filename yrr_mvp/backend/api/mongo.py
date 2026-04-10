import os
from pymongo import MongoClient


def get_mongo_db():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise RuntimeError("MONGODB_URI environment variable is not set")

    db_name = os.getenv("MONGODB_DB", "yrr_mvp")
    client = MongoClient(uri)
    return client[db_name]
