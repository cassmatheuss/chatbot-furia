from pymongo import MongoClient

def connect_mongodb(url, db_name):
    client = MongoClient(url)
    db = client[db_name]
    return db