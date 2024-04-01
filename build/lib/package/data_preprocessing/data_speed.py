import numpy as np
import pandas as pd

# Load the data
data_path = '../../data/processed/cleaned_night.csv'
data = pd.read_csv(data_path)

# Converting the 'Time' column from object (string) to datetime
data['Time'] = pd.to_datetime(data['Time'])

# Verify the change by checking data types again
updated_data_types = data.dtypes
print(updated_data_types)

# Sorting data
sorted_data = data.sort_values(by=['Line', 'Brigade', 'Time'])

# Calculate differences in lat, lon, and time within each group
sorted_data['lat_shifted'] = sorted_data.groupby(['Line', 'Brigade'])['Lat'].shift(-1)
sorted_data['lon_shifted'] = sorted_data.groupby(['Line', 'Brigade'])['Lon'].shift(-1)
sorted_data['time_diff'] = (sorted_data.groupby(['Line', 'Brigade'])['Time'].shift(-1) - sorted_data[
    'Time']).dt.total_seconds() / 3600  # hours


# Define a vectorized function to calculate distances using the haversine formula
def calculate_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth using haversine formula (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6371 * c  # Radius of earth in kilometers.
    return km


# Calculate distances for rows with valid next positions
valid_rows = sorted_data.dropna(subset=['lat_shifted', 'lon_shifted'])

# Calculate the distances between consecutive points for each Line and Brigade
valid_rows['distance'] = calculate_distance(
    valid_rows['Lon'], valid_rows['Lat'],
    valid_rows['lon_shifted'], valid_rows['lat_shifted']
)

# Re-calculate speeds using the distances and time differences
valid_rows['Speed (km/h)'] = valid_rows['distance'] / valid_rows['time_diff']

# Cleanup: remove temporary columns and handle rows without speed calculation
sorted_data = sorted_data.drop(columns=['lat_shifted', 'lon_shifted', 'time_diff'])
sorted_data.loc[valid_rows.index, 'Speed (km/h)'] = valid_rows['Speed (km/h)']

# Cleanup: remove rows with speed above 90 km/h
sorted_data = sorted_data.loc[sorted_data['Speed (km/h)'] <= 90]

# Save the data with speed column
speed_data_path = '../../data/processed/speed_added_night.csv'
sorted_data.to_csv(speed_data_path, index=False)
