import requests
import pandas as pd
import time

# Configuration
API_KEY = 'f7d6e298-db1d-4b07-aca0-af9e82319374'
RESOURCE_ID = 'f2e5503e-927d-4ad3-9500-4ab9e55deb59'
BASE_URL = 'https://api.um.warszawa.pl/api/action/busestrams_get/'

# Parameters
vehicle_type = 1  # 1 for buses, 2 for trams


# Function to collect data
def fetch_vehicle_data(vehicle_type, line=None, brigade=None, interval=60, duration=3600):
    """
    Fetches vehicle data for a specified duration and interval.

    :param vehicle_type: Type of vehicle (1 for buses, 2 for trams)
    :param line: Specific line number (optional)
    :param brigade: Specific brigade number (optional)
    :param interval: Interval between API calls in seconds
    :param duration: Total duration to collect data in seconds
    """
    end_time = time.time() + duration
    data = []
    i = 1  # Initialize counter
    while time.time() < end_time:
        try:
            params = {
                'resource_id': RESOURCE_ID,
                'apikey': API_KEY,
                'type': vehicle_type,
                'line': line,
                'brigade': brigade
            }
            response = requests.post(BASE_URL, params=params)

            if response.status_code == 200:
                vehicles = response.json()['result']
                if isinstance(vehicles, list):
                    for vehicle in vehicles:
                        data.append({
                            'Lat': vehicle['Lat'],
                            'Lon': vehicle['Lon'],
                            'Time': vehicle['Time'],
                            'Line': vehicle['Lines'],
                            'Brigade': vehicle['Brigade']
                        })
                print(f"Interval {i}: Data fetched successfully.")
            else:
                print(f"Interval {i}: Failed to fetch data: HTTP {response.status_code}")
        except Exception as e:
            print(f"Interval {i}: An error occurred: {e}")
        finally:
            i += 1  # Increment counter
            time.sleep(interval)
    return pd.DataFrame(data)


data_frame = fetch_vehicle_data(vehicle_type=1, interval=60, duration=3600)

csv_file_name = '../../data/raw/raw_data_afternoon.csv'

data_frame.to_csv(csv_file_name, index=False)

print(f'Data saved to {csv_file_name}')
