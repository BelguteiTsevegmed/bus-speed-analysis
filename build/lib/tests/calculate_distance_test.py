import unittest
import package.data_preprocessing.data_speed as my_package


class TestCalculateDistance(unittest.TestCase):
    def test_distance_calculation(self):
        # Test coordinates between two points known distance apart
        lon1, lat1 = -73.985428, 40.748817  # Empire State Building
        lon2, lat2 = -73.985656, 40.748433  # Somewhere close to Empire State Building

        # Known distance between these points in meters (roughly)
        known_distance_km = 0.043

        # Calculate the distance using the function
        distance = my_package.calculate_distance(lon1, lat1, lon2, lat2)

        # Verify the distance is as expected
        self.assertAlmostEqual(distance, known_distance_km, places=2,
                               msg="The calculated distance does not match the known distance")


if __name__ == '__main__':
    unittest.main()
