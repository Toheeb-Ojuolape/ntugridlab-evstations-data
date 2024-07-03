import json
import pandas as pd
import os

# Directory containing the JSON files
input_dir = './jpl_weather_data'
output_dir = 'jpl_weather_monthly_data'
os.makedirs(output_dir, exist_ok=True)

# Initialize lists to store the combined data
date_list = []
mintemp_list = []
maxtemp_list = []
avgtemp_list = []
precip_list = []
humidity_list = []
wind_speed_list = []

# Loop through all JSON files in the directory
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract historical data
        historical_data = data['historical']

        # Parse the historical data
        for date, details in historical_data.items():
            date_list.append(date)
            mintemp_list.append(details['mintemp'])
            maxtemp_list.append(details['maxtemp'])
            avgtemp_list.append(details['avgtemp'])
            daily_precip = []
            daily_humidity = []
            daily_wind_speed = []
            for hourly in details['hourly']:
                daily_precip.append(hourly['precip'])
                daily_humidity.append(hourly['humidity'])
                daily_wind_speed.append(hourly['wind_speed'])
            precip_list.append(sum(daily_precip) / len(daily_precip))
            humidity_list.append(sum(daily_humidity) / len(daily_humidity))
            wind_speed_list.append(sum(daily_wind_speed) / len(daily_wind_speed))

# Create a DataFrame
df = pd.DataFrame({
    'Date': date_list,
    'MinTemp': mintemp_list,
    'MaxTemp': maxtemp_list,
    'AvgTemp': avgtemp_list,
    'AvgPrecipitation': precip_list,
    'AvgHumidity': humidity_list,
    'AvgWindSpeed': wind_speed_list
})

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Group by month and calculate the required statistics
monthly_stats = df.resample('M', on='Date').agg({
    'MinTemp': 'min',
    'MaxTemp': 'max',
    'AvgTemp': 'mean',
    'AvgPrecipitation': 'mean',
    'AvgHumidity': 'mean',
    'AvgWindSpeed': 'mean'
}).reset_index()

# Save the result to a CSV file
output_file = os.path.join(output_dir, "monthly_weather_data.csv")
monthly_stats.to_csv(output_file, index=False)

print(f"Monthly weather statistics have been saved to {output_file}")
