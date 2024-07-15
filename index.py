import json
import os
import pandas as pd
from datetime import datetime

# Function to load data from a JSON file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to process and save data
def process_and_save_data(data):
    # Check if data is in the correct format (list of dictionaries)
    if isinstance(data, dict) and "_items" in data:
        data = data["_items"]
    elif not isinstance(data, list):
        raise ValueError("The input data must be a list of dictionaries or a dictionary containing an '_items' key.")

    # Load data into a pandas DataFrame
    df = pd.DataFrame(data)

    # Convert connectionTime and disconnectTime to datetime
    df['connectionTime'] = pd.to_datetime(df['connectionTime'], utc=True)
    df['disconnectTime'] = pd.to_datetime(df['disconnectTime'], utc=True)

    # Extract the month from connectionTime
    df['month'] = df['connectionTime'].dt.to_period('M')

    # Group by month, siteID, stationID, timezone, and spaceID, and sum kWhDelivered
    grouped = df.groupby(['month', 'siteID', 'stationID', 'timezone', 'spaceID']).agg({'kWhDelivered': 'sum'}).reset_index()

    # Create a directory to store the output CSV files
    output_dir = "caltech_stations_data"
    os.makedirs(output_dir, exist_ok=True)

    # Save each stationID's data to a separate CSV file
    for station_id, station_df in grouped.groupby('stationID'):
        station_df.to_csv(os.path.join(output_dir, f"{station_id}.csv"), index=False)

    print("CSV files created successfully in the 'caltech_stations_data' directory.")

# Main script
if __name__ == "__main__":
    # Path to the input JSON file
    input_file_path = './acndata_sessions.json'

    # Load data from the JSON file
    data = load_json(input_file_path)
    # Process the data and save to individual CSV files
    process_and_save_data(data)
