from pymongo import MongoClient

client = MongoClient("mongodb://root:example@localhost:27017")
db = client["zipstats"]
collection = db["zips"]

# a) States with total population over 10 million
def task_a():
    return list(collection.aggregate([
        {"$group": {"_id": "$state_name", "totalPop": {"$sum": "$population"}}},
        {"$match": {"totalPop": {"$gt": 10_000_000}}},
        {"$sort": {"totalPop": -1}}
    ]))

# b) Average city population by state
def task_b():
    return list(collection.aggregate([
        {"$group": {"_id": {"state": "$state_name", "city": "$city"}, "cityPop": {"$sum": "$population"}}},
        {"$group": {"_id": "$_id.state", "avgCityPop": {"$avg": "$cityPop"}}},
        {"$sort": {"avgCityPop": -1}}
    ]))

# c) Largest and smallest city in each state
def task_c():
    return list(collection.aggregate([
        {"$group": {"_id": {"state": "$state_name", "city": "$city"}, "pop": {"$sum": "$population"}}},
        {"$sort": {"pop": -1}},
        {"$group": {
            "_id": "$_id.state",
            "largestCity": {"$first": {"city": "$_id.city", "pop": "$pop"}},
            "smallestCity": {"$last": {"city": "$_id.city", "pop": "$pop"}}
        }}
    ]))

# d) Largest and smallest county in each state
def task_d():
    return list(collection.aggregate([
        {"$group": {"_id": {"state": "$state_name", "county": "$county_name"}, "pop": {"$sum": "$population"}}},
        {"$sort": {"pop": -1}},
        {"$group": {
            "_id": "$_id.state",
            "largestCounty": {"$first": {"county": "$_id.county", "pop": "$pop"}},
            "smallestCounty": {"$last": {"county": "$_id.county", "pop": "$pop"}}
        }}
    ]))

# e) Nearest 10 zips to Willis Tower
def task_e():
    return list(collection.find({
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [-87.635918, 41.878876]}
            }
        }
    }).limit(10))

# f) Total population between 50–200km of Statue of Liberty
def task_f():
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

# Run all and print a few entries
print("a)", task_a())
print("b)", task_b()[:5])
print("c)", task_c()[:3])
print("d)", task_d()[:3])
print("e)", task_e()[:3])
print("f)", task_f())
