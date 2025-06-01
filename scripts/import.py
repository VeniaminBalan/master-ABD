import csv
from pymongo import MongoClient, GEOSPHERE

client = MongoClient("mongodb://root:example@localhost:27017")
db = client["zipstats"]
collection = db["zips"]

try:
    collection.drop()  # clean old data
    print("Collection dropped successfully.")
except Exception as e:
    print(f"Error dropping collection: {e}")

with open("simplemaps/uszips.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row["lat"] or not row["lng"]:
            continue  # skip incomplete rows
        doc = {
            "zip": row["zip"],
            "lat": float(row["lat"]),
            "lng": float(row["lng"]),
            "city": row["city"],
            "state_id": row["state_id"],
            "state_name": row["state_name"],
            "population": int(row["population"]) if row["population"] else 0,
            "county_name": row["county_name"],
            "location": {
                "type": "Point",
                "coordinates": [float(row["lng"]), float(row["lat"])]
            }
        }
        collection.insert_one(doc)

collection.create_index([("state_name", 1)])
collection.create_index([("city", 1)])
collection.create_index([("county_name", 1)])
collection.create_index([("population", -1)])
collection.create_index([("location", GEOSPHERE)])

print("CSV data loaded and indexes created.")
