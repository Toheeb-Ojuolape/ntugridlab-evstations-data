import requests
import json
import os
from datetime import datetime, timedelta

# Your Weatherstack API key
API_KEY = "YOUR_API_KEY"

# Function to fetch historical weather data
def fetch_historical_weather(location, start_date, end_date):
    url = f"http://api.weatherstack.com/historical"
    params = {
        'access_key': API_KEY,
        'query': location,
        'historical_date_start': start_date,
        'historical_date_end': end_date,
        'hourly': 1,  # Daily data
    }
    response = requests.get(url, params=params)
    return response.json()

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to save data to a file
def save_data_to_file(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# Main script to fetch data every 60 days from 2018-04-01 to 2024-06-01
if __name__ == "__main__":
    location = 91125 # this is the zipcode for caltech
    start_date = datetime(2018, 9, 1)
    end_date = datetime(2024, 6, 1)
    delta = timedelta(days=60)
    
    current_date = start_date
    output_dir = "jpl_weather_data"
    create_directory(output_dir)
    
    while current_date < end_date:
        next_date = current_date + delta
        if next_date > end_date:
            next_date = end_date
        
        period_start = current_date.strftime('%Y-%m-%d')
        period_end = (next_date - timedelta(days=1)).strftime('%Y-%m-%d')
        period_name = f"{current_date.strftime('%b-%Y')}_to_{(next_date - timedelta(days=1)).strftime('%b-%Y')}"
        file_name = os.path.join(output_dir, f"{period_name}.json")
        
        print(f"Fetching data from {period_start} to {period_end}")
        data = fetch_historical_weather(location, period_start, period_end)
        save_data_to_file(data, file_name)
        
        current_date = next_date

    print("Weather data fetched and saved successfully in the 'weather_data' directory.")
