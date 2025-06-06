# Scripts Documentation

This folder contains scripts essential for setting up and running the MongoDB US ZIPs dataset project. Below is an explanation of the `import.py` script and the indexes it creates.

## `import.py`

### Purpose
The `import.py` script is responsible for importing the US ZIPs dataset (`uszips.csv`) into a MongoDB collection. It also creates indexes to optimize query performance.

### Workflow
1. **Connect to MongoDB**:
   - Establishes a connection to the MongoDB instance using the `pymongo` library.
   - Connects to the `zipstats` database and the `zips` collection.

2. **Clean Existing Data**:
   - Drops the `zips` collection if it exists to ensure a clean import.

3. **Read and Parse CSV**:
   - Reads the `uszips.csv` file using Python's `csv.DictReader`.
   - Skips rows with missing latitude or longitude values.
   - Converts relevant fields (e.g., `lat`, `lng`, `population`) to appropriate data types.

4. **Insert Documents**:
   - Inserts each row as a document into the `zips` collection.
   - Adds a `location` field with GeoJSON format for geospatial queries.

5. **Create Indexes**:
   - Creates indexes to optimize query performance (explained below).

6. **Print Status**:
   - Prints a success message after loading the data and creating indexes.

### Code Snippet
```python
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
```

## Indexes Created

### 1. State and City Index
```python
collection.create_index([("state_name", 1)])
collection.create_index([("city", 1)])
```
- **Purpose**: Optimizes queries that filter by state and city.
- **Fields**: `state_name` (ascending), `city` (ascending).

### 2. County Name Index
```python
collection.create_index([("county_name", 1)])
```
- **Purpose**: Improves performance for queries filtering by county name.
- **Field**: `county_name` (ascending).

### 3. Population Index
```python
collection.create_index([("population", -1)])
```
- **Purpose**: Speeds up queries that sort or filter by population.
- **Field**: `population` (descending).

### 4. Geospatial Index
```python
collection.create_index([("location", GEOSPHERE)])
```
- **Purpose**: Enables geospatial queries, such as finding documents near a specific location.
- **Field**: `location` (GeoJSON format).
