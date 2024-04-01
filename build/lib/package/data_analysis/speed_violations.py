import pandas as pd

# Load the data
file_path = '../../data/processed/speed_added_night.csv'
data = pd.read_csv(file_path)

# Convert Time to datetime and sort data by Line, Brigade, and Time
data['Time'] = pd.to_datetime(data['Time'])
sorted_data = data.sort_values(by=['Line', 'Brigade', 'Time'])

speed_limit = 50
sorted_data['Speed Violation'] = sorted_data['Speed (km/h)'] > speed_limit

# Count unique buses that have at least one speed violation
violations_data = sorted_data[sorted_data['Speed Violation']]
unique_buses_violating_speed_limit = violations_data[['Line', 'Brigade']].drop_duplicates().shape[0]

print(unique_buses_violating_speed_limit)
