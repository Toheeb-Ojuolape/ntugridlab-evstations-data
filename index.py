import json
import os
from collections import defaultdict

# Function to load data from a JSON file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to group data by stationID and save to individual JSON files
def group_and_save_data(data):
    # Extract the list of items
    items = data["_items"]

    # Group data by stationID
    grouped_data = defaultdict(list)
    for record in items:
        station_id = record["stationID"]
        grouped_data[station_id].append(record)

    # Create a directory to store the output JSON files
    output_dir = "jpl_stations_data"
    os.makedirs(output_dir, exist_ok=True)

    # Write each group to a separate JSON file
    for station_id, records in grouped_data.items():
        file_path = os.path.join(output_dir, f"{station_id}.json")
        with open(file_path, 'w') as json_file:
            json.dump(records, json_file, indent=4)

    print("JSON files created successfully in the 'JPL stations_data' directory.")

# Main script
if __name__ == "__main__":
    # Path to the input JSON file
    input_file_path = './jpl.json'

    # Load data from the JSON file
    data = load_json(input_file_path)

    # Group the data by stationID and save to individual JSON files
    group_and_save_data(data)
