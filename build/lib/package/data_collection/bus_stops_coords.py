import requests
import pandas as pd


def retrieve_bus_stops_to_dataframe(api_key, bus_stop_name):
    """
    Retrieve information about bus stops by name and load it into a pandas DataFrame.

    Parameters:
    - api_key: Your API key for the DBtimetable API.
    - bus_stop_name: The name of the bus stop to retrieve information for.

    Returns:
    A pandas DataFrame containing bus stop information.
    """

    bus_stop_name_encoded = requests.utils.quote(bus_stop_name)

    url = f"https://api.um.warszawa.pl/api/action/dbtimetable_get?id=b27f4c17-5c50-4a5b-89dd-236b282bc499&name={bus_stop_name_encoded}&apikey={api_key}"

    # Make the GET request to the API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        values_list = [item['values'] for item in data['result']]

        df_list = []
        for values in values_list:
            values_dict = {d['key']: d['value'] for d in values}
            df_list.append(pd.DataFrame([values_dict]))

        df_bus_stops = pd.concat(df_list, ignore_index=True)

        return df_bus_stops
    else:
        print("Failed to retrieve data")
        return pd.DataFrame()


# Example usage
api_key = "f7d6e298-db1d-4b07-aca0-af9e82319374"
bus_stop_name = "Marszałkowska"
df_bus_stops = retrieve_bus_stops_to_dataframe(api_key, bus_stop_name)

print(df_bus_stops)
