# States with total population over 10 million
from db_connection import get_db_connection

def execute():
    """
    States with total population over 10 million
    """
    _, collection = get_db_connection()
    return list(collection.aggregate([
        {"$group": {"_id": "$state_name", "totalPop": {"$sum": "$population"}}},
        {"$match": {"totalPop": {"$gt": 10_000_000}}},
        {"$sort": {"totalPop": -1}}
    ]))


print(execute())