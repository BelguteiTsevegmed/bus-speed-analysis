import unittest
from unittest.mock import patch
import pandas as pd
import package.data_collection.online_position as my_package


class TestFetchVehicleData(unittest.TestCase):

    @patch('requests.post')
    def test_successful_api_call_and_data_structure(self, mock_post):
        # Mock the API response
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': [
                {'Lat': '52.229', 'Lon': '21.012', 'Time': '10:00', 'Lines': '102', 'Brigade': '1'}
            ]
        }

        # Call the function
        df = my_package.fetch_vehicle_data(vehicle_type=1, interval=10, duration=60)

        # Verify the DataFrame structure
        expected_columns = ['Lat', 'Lon', 'Time', 'Line', 'Brigade']
        self.assertTrue(all(column in df.columns for column in expected_columns),
                        "DataFrame should contain expected columns")
        self.assertIsInstance(df, pd.DataFrame, "Function should return a pandas DataFrame")

    @patch('requests.post')
    def test_api_call_failure_handling(self, mock_post):
        # Mock the API response
        mock_response = mock_post.return_value
        mock_response.status_code = 400

        # Call the function expecting no exceptions and an empty DataFrame
        df = my_package.fetch_vehicle_data(vehicle_type=1, interval=10, duration=60)

        # Check if the DataFrame is empty as expected
        self.assertTrue(df.empty, "DataFrame should be empty on API call failure")
        self.assertEqual(len(df), 0, "DataFrame should have no rows on API call failure")


if __name__ == '__main__':
    unittest.main()
