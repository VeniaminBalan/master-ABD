# Largest and smallest city in each state
from db_connection import get_db_connection

def execute():
    """
    Largest and smallest city in each state
    """
    _, collection = get_db_connection()
    return list(collection.aggregate([
        {"$group": {"_id": {"state": "$state_name", "city": "$city"}, "pop": {"$sum": "$population"}}},
        {"$sort": {"pop": -1}},
        {"$group": {
            "_id": "$_id.state",
            "largestCity": {"$first": {"city": "$_id.city", "pop": "$pop"}},
            "smallestCity": {"$last": {"city": "$_id.city", "pop": "$pop"}}
        }}
    ]))

print(execute())