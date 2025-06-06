# 📘 MongoDB US ZIPs Dataset Project — Documentation

## 1. Overview

The objective of this project is to demonstrate proficiency with MongoDB by performing various statistical and geospatial operations on a dataset of U.S. ZIP codes. The dataset contains approximately 33,000 entries and is already included in this repository.

## 2. How to Run the Project

### Prerequisites
1. **Dataset**:
   - The dataset `uszips.csv` is already included in the `scripts/simplemaps/` directory.

2. **Install Docker**:
   - Ensure Docker is installed and running on your system.

3. **Install Python**:
   - Install Python 3.10 or later.
   - Install `pip`, the Python package manager, if not already installed.

### Steps to Run

#### 1. Start MongoDB with Docker
Run the following command to start a MongoDB instance using Docker:
```bash
cd <project-directory>
docker-compose up -d
```
This will start a MongoDB container with the configuration specified in `compose.yml`.

#### 2. Install Python Dependencies
Navigate to the `scripts/` directory and install the required Python packages:
```bash
cd scripts
pip install -r requirements.txt
```

#### 3. Import the Dataset into MongoDB
Run the following script to import the dataset into MongoDB:
```bash
python import.py
```
This script reads the `uszips.csv` file and imports it into the `zips` collection in the `zipstats` database.

#### 4. Run Tasks
Each task is implemented as a separate Python script in the `tasks/` directory. You can run them from the terminal as follows:

- **Task A**: States with total population over 10 million
  ```bash
  python tasks/task_a.py
  ```

- **Task B**: Average city population by state
  ```bash
  python tasks/task_b.py
  ```

- **Task C**: Largest and smallest city in each state
  ```bash
  python tasks/task_c.py
  ```

- **Task D**: Largest and smallest counties in each state
  ```bash
  python tasks/task_d.py
  ```

- **Task E**: Nearest 10 zips to Willis Tower
  ```bash
  python tasks/task_e.py
  ```

- **Task F**: Total population between 50–200 km of the Statue of Liberty
  ```bash
  python tasks/task_f.py
  ```

### Notes
- Ensure the MongoDB instance is running before executing any tasks.
- Use the `docker-compose down` command to stop the MongoDB container when done.

---
