# Task Documentation

This document provides an overview of the tasks implemented in this project, including the initial approach, any failed attempts, and lessons learned that led to the final solution.

## Task A: States with Total Population Over 10 Million

### Requirement
Retrieve states with a total population of over 10 million.

### Approach
- Grouped documents by `state_name`.
- Summed the `population` field for each state.
- Filtered states with a total population greater than 10 million.
- Sorted the results in descending order of population.

### Lessons Learned
- MongoDB's `$group` and `$match` stages are powerful for aggregation tasks.
- Sorting after filtering ensures efficient query execution.

---

## Task B: Average City Population by State

### Requirement
Calculate the average city population by state.

### Approach
- Grouped documents by `state_name` and `city` to calculate city populations.
- Grouped by `state_name` again to calculate the average city population.
- Added support for filtering by a specific state.

### Lessons Learned
- Nested grouping is essential for hierarchical data aggregation.
- Adding optional parameters (e.g., `state`) makes the function more versatile.

---

## Task C: Largest and Smallest City in Each State

### Requirement
Identify the largest and smallest city in each state.

### Approach
- Grouped documents by `state_name` and `city` to calculate city populations.
- Sorted cities by population in descending order.
- Used `$first` and `$last` to extract the largest and smallest cities for each state.

### Lessons Learned
- Sorting before grouping allows efficient extraction of extreme values.

---

## Task D: Largest and Smallest Counties in Each State

### Requirement
Identify the largest and smallest counties in each state.

### Approach
- Grouped documents by `state_name` and `county_name` to calculate county populations.
- Sorted counties by population in descending order.
- Used `$first` and `$last` to extract the largest and smallest counties for each state.

### Lessons Learned
- The approach is similar to Task C, demonstrating the reusability of aggregation patterns.

---

## Task E: Nearest 10 Zips to Willis Tower

### Requirement
Retrieve the nearest 10 zips to Willis Tower (coordinates: 41.878876, -87.635918).

### Approach
- Used the `$near` operator to find documents closest to the specified coordinates.
- Limited the results to 10 documents.

### Lessons Learned
- MongoDB's geospatial queries are efficient for proximity-based tasks.
- Proper indexing on location fields is crucial for performance.

---

## Task F: Total Population Between 50–200 km of the Statue of Liberty

### Requirement
Calculate the total population situated between 50 and 200 km of the Statue of Liberty (coordinates: 40.689247, -74.044502).

### Approach
- Used the `$geoNear` operator to find documents within the specified distance range.
- Summed the `population` field for the matching documents.

### Lessons Learned
- `$geoNear` is versatile for distance-based filtering.
- Combining `$geoNear` with `$group` enables complex geospatial aggregations.

---

This documentation serves as a reference for understanding the implementation and thought process behind each task.
