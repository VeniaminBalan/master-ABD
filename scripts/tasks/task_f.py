# Total population between 50–200km of Statue of Liberty
from db_connection import get_db_connection

def execute():
    """
    Total population between 50–200km of Statue of Liberty
    """
    _, collection = get_db_connection()
    return list(collection.aggregate([
        {
            "$geoNear": {
                "near": {"type": "Point", "coordinates": [-74.044502, 40.689247]},
                "distanceField": "dist",
                "spherical": True,
                "minDistance": 50 * 1000,
                "maxDistance": 200 * 1000
            }
        },
        {"$group": {"_id": None, "totalPop": {"$sum": "$population"}}}
    ]))

print(execute())