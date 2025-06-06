# MongoDB connection configuration
from pymongo import MongoClient

def get_db_connection():
    """
    Establish connection to MongoDB and return database and collection objects
    """
    client = MongoClient("mongodb://root:example@localhost:27017")
    db = client["zipstats"]
    collection = db["zips"]
    return db, collection
