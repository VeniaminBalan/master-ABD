# Average city population by state
from db_connection import get_db_connection

def execute(state=None):
    """
    Average city population by state
    
    Parameters:
    state (str, optional): State name to filter results. If None, returns data for all states.
    
    Returns:
    list: List of dictionaries containing state name and average city population.
          If state is specified, returns average city population for that state.
    """
    _, collection = get_db_connection()
    
    if state is None:
        # Get average city population for all states
        return list(collection.aggregate([
            {"$group": {"_id": {"state": "$state_name", "city": "$city"}, "cityPop": {"$sum": "$population"}}},
            {"$group": {"_id": "$_id.state", "avgCityPop": {"$avg": "$cityPop"}}},
            {"$sort": {"avgCityPop": -1}}
        ]))
    else:
        # Get average city population for the specified state
        return list(collection.aggregate([
            {"$match": {"state_name": state}},
            {"$group": {"_id": {"state": "$state_name", "city": "$city"}, "cityPop": {"$sum": "$population"}}},
            {"$group": {"_id": "$_id.state", "avgCityPop": {"$avg": "$cityPop"}}},
            {"$project": {"_id": 0, "state": "$_id", "averageCityPopulation": "$avgCityPop"}}
        ]))


state = input("Enter state name ex: California (or press Enter for all states): ").strip()
print(execute(state))