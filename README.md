
# 📘 MongoDB US ZIPs Dataset Project — Documentation

## 1. Overview

The objective of this project is to demonstrate proficiency with MongoDB by performing various statistical and geospatial operations on a dataset of U.S. ZIP codes. The dataset was obtained from [SimpleMaps US ZIP Codes](https://simplemaps.com/data/us-zips) and contains approximately 33,000 entries.

---

## 2. Importing the CSV File

### 📂 Data Source
- Dataset: Free tier of the U.S. ZIP codes dataset from SimpleMaps.
- Format: CSV file with fields such as `zip`, `lat`, `lng`, `city`, `state_id`, `state_name`, `population`, `county_name`, etc.

### 🧰 Tools Used
- Python with `pandas` and `pymongo` libraries.
- MongoDB (locally hosted or replica set depending on availability).

### 📈 Import Strategy
- Used `pandas.read_csv()` to load the file and convert it into JSON-like documents.
- Inserted documents into MongoDB using `pymongo`.

```python
import pandas as pd
from pymongo import MongoClient

df = pd.read_csv("uszips.csv")
df = df.fillna("")  # Replace NaNs with empty strings
docs = df.to_dict(orient="records")

client = MongoClient("mongodb://localhost:27017/")
db = client["us_zips"]
collection = db["zips"]
collection.insert_many(docs)
```

### 🧠 Decision Points
- Filled missing values to avoid insert errors.
- Used descriptive field names (`state_name`, `county_name`) for query clarity.
- Considered indexing before running performance-heavy queries.

---

## 3. Indexing Strategy

### 🧭 Geospatial Index
Created a new `location` field from `lat` and `lng`:
```python
collection.update_many({}, [{"$set": {"location": {"type": "Point", "coordinates": ["$lng", "$lat"]}}}])
collection.create_index([("location", "2dsphere")])
```

### 📊 Other Indexes
- `state_name`: for grouping operations and filtering.
- `city`: for city-based population aggregation.
- `county_name`: for county-based statistics.
- `population`: for range queries.

Example:
```python
collection.create_index("state_name")
collection.create_index("city")
collection.create_index("county_name")
collection.create_index("population")
```

### 🧪 Justification
Indexes significantly improved performance for aggregation pipelines and geospatial queries. These were verified using `.explain("executionStats")`.

---

## 4. Task-by-Task Documentation

### ✅ a) States with a Total Population Over 10 Million

```python
[
  {"$group": {"_id": "$state_name", "total_pop": {"$sum": "$population"}}},
  {"$match": {"total_pop": {"$gt": 10_000_000}}},
  {"$sort": {"total_pop": -1}}
]
```

### ✅ b) Average City Population by State

```python
[
  {"$group": {"_id": {"state": "$state_name", "city": "$city"}, "city_pop": {"$sum": "$population"}}},
  {"$group": {"_id": "$_id.state", "avg_city_pop": {"$avg": "$city_pop"}}},
  {"$sort": {"avg_city_pop": -1}}
]
```

### ✅ c) Largest and Smallest City in Each State

```python
[
  {"$group": {"_id": {"state": "$state_name", "city": "$city"}, "pop": {"$sum": "$population"}}},
  {"$sort": {"_id.state": 1, "pop": 1}},
  {"$group": {
      "_id": "$_id.state",
      "smallest_city": {"$first": {"city": "$_id.city", "population": "$pop"}},
      "largest_city": {"$last": {"city": "$_id.city", "population": "$pop"}}
  }}
]
```

### ✅ d) Largest and Smallest County in Each State

```python
[
  {"$group": {"_id": {"state": "$state_name", "county": "$county_name"}, "pop": {"$sum": "$population"}}},
  {"$sort": {"_id.state": 1, "pop": 1}},
  {"$group": {
      "_id": "$_id.state",
      "smallest_county": {"$first": {"county": "$_id.county", "population": "$pop"}},
      "largest_county": {"$last": {"county": "$_id.county", "population": "$pop"}}
  }}
]
```

### ✅ e) Nearest 10 ZIPs to Willis Tower

```python
{
  "location": {
    "$near": {
      "$geometry": {
        "type": "Point",
        "coordinates": [-87.635918, 41.878876]
      }
    }
  }
}
```

### ✅ f) Total Population between 50km and 200km around Statue of Liberty

```python
[
  {
    "$geoNear": {
      "near": {"type": "Point", "coordinates": [-74.044502, 40.689247]},
      "distanceField": "dist.calculated",
      "spherical": True,
      "minDistance": 50 * 1000,
      "maxDistance": 200 * 1000
    }
  },
  {
    "$group": {
      "_id": None,
      "total_population": {"$sum": "$population"}
    }
  }
]
```

---

## 5. Final Remarks

### 🔍 Performance & Indexing Summary
- Without indexes, performance was sluggish on large groupings.
- Indexes on `state_name`, `city`, `county_name`, and `location` proved essential.
- Geospatial queries required a `2dsphere` index and adding a `location` field.

### 📘 What I Learned
- How to import CSV data robustly into MongoDB using Python.
- Importance of indexing and using `.explain()` for query tuning.
- Deep understanding of `$group`, `$geoNear`, and nested aggregations.
