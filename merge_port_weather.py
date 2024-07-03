import pandas as pd
import os

# Directories
stations_data_dir = './jpl_stations_data'
weather_data_file = './jpl_weather_monthly_data/monthly_weather_data.csv'
output_dir = './jpl_model_data'
os.makedirs(output_dir, exist_ok=True)

# Load the monthly weather data
weather_data = pd.read_csv(weather_data_file)
weather_data['month'] = pd.to_datetime(weather_data['month']).dt.to_period('M')  # Convert to YYYY-MM format

# Loop through each station data file
for filename in os.listdir(stations_data_dir):
    if filename.endswith('.csv'):
        station_file_path = os.path.join(stations_data_dir, filename)
        
        # Load the station data
        station_data = pd.read_csv(station_file_path)
        station_data['month'] = pd.to_datetime(station_data['month']).dt.to_period('M')  # Convert to YYYY-MM format
        
        # Merge with the weather data
        merged_data = pd.merge(station_data, weather_data, on='month', how='left')
        
        # Save the merged data
        station_id = filename.split('.')[0]  # Assuming the filename format is <stationID>.csv
        output_file_path = os.path.join(output_dir, f"{station_id.strip()}.csv")
        merged_data.to_csv(output_file_path, index=False)

print(f"Merged data has been saved to {output_dir}")
