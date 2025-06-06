# Largest and smallest county in each state
from db_connection import get_db_connection

def execute():
    """
    Largest and smallest county in each state
    """
    _, collection = get_db_connection()
    return list(collection.aggregate([
        {"$group": {"_id": {"state": "$state_name", "county": "$county_name"}, "pop": {"$sum": "$population"}}},
        {"$sort": {"pop": -1}},
        {"$group": {
            "_id": "$_id.state",
            "largestCounty": {"$first": {"county": "$_id.county", "pop": "$pop"}},
            "smallestCounty": {"$last": {"county": "$_id.county", "pop": "$pop"}}
        }}
    ]))

print(execute())