import unittest
import os
import django
import requests
from unittest.mock import patch
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_analysis.settings')
django.setup()
from weather.models import WeatherData
from fetch_data import fetch_and_store_weather_data


class TestWeatherDataFetching(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_and_store_weather_data_success(self, mock_get):
        mock_response = {
            'coord': {'lon': -0.1257, 'lat': 51.5085},
            'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}],
            'base': 'stations',
            'main': {'temp': 6.51, 'feels_like': 3.4, 'temp_min': 5.27, 'temp_max': 7.2, 'pressure': 1011, 'humidity': 90},
            'visibility': 10000,
            'wind': {'speed': 4.63, 'deg': 140},
            'clouds': {'all': 40},
            'dt': 1701930463,
            'sys': {'type': 2, 'id': 2075535, 'country': 'GB', 'sunrise': 1701935478, 'sunset': 1701964357},
            'timezone': 0,
            'id': 2643743,
            'name': 'London',
            'cod': 200
        }
        mock_get.return_value.json.return_value = mock_response

        with self.assertLogs('server.log', level='INFO') as log:
            fetch_and_store_weather_data('mock_api_key', ['London'])
            self.assertTrue(log.output, 'No logs found in INFO level')

        weather_data = WeatherData.objects.get(city='London')
        self.assertEqual(weather_data.temperature, 6.51)
        self.assertEqual(weather_data.humidity, 90)
        self.assertEqual(weather_data.wind_speed, 4.63)
        self.assertEqual(weather_data.city_lat, 51.5085)
        self.assertEqual(weather_data.city_lon, -0.1257)

    @patch('requests.get')
    def test_fetch_and_store_weather_data_failure(self, mock_get):
        # Simulate a RequestException
        mock_get.side_effect = requests.RequestException('Connection error')
        with self.assertLogs('server.log', level='ERROR') as log:
            fetch_and_store_weather_data('mock_api_key', ['InvalidCity'])
            self.assertTrue(log.output, 'No logs found in ERROR level')
            self.assertIn('Error fetching data for InvalidCity:', log.output[0])

        # Simulate a JSONDecodeError
        mock_get.return_value.json.side_effect = ValueError('Invalid JSON')
        with self.assertLogs('server.log', level='ERROR') as log:
            fetch_and_store_weather_data('mock_api_key', ['InvalidCity'])
            self.assertTrue(log.output, 'No logs found in ERROR level')
            self.assertIn('Error decoding JSON for InvalidCity:', log.output[0])

if __name__ == '__main__':
    unittest.main()


