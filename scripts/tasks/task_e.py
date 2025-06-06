# Nearest 10 zips to Willis Tower
from db_connection import get_db_connection

def execute():
    """
    Nearest 10 zips to Willis Tower
    """
    _, collection = get_db_connection()
    return list(collection.find({
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [-87.635918, 41.878876]}
            }
        }
    }).limit(10))

print(execute())