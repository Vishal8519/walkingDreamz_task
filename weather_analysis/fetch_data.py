import os,django
import requests
from requests.exceptions import RequestException, JSONDecodeError
import logging
from django.conf import settings
logging.basicConfig(filename='server.log', level=logging.INFO)
import os, re, time, django, json
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_analysis.settings')
django.setup()

from weather.models import *

def fetch_and_store_weather_data(api_key, cities):
    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()
        print(data)   # added for line just for debug
        logging.info(f"Successfully fetched and stored data for {city}.")
        
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except RequestException as e:
            logging.error(f'Error fetching data for {city}: {e}')
            continue
        except JSONDecodeError as e:
            logging.error(f'Error decoding JSON for {city}: {e}')
            continue

        print(data)
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        lat = data['coord']['lat']
        lon = data['coord']['lon']

        WeatherData.objects.create(
            city=city,
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            city_lon=lon,
            city_lat=lat
        )

        print(f'Successfully fetched and stored data for {city}.')

if __name__ == "__main__":

    api_key = settings.API_KEY
    cities = ["London", "New York", "Tokyo", "Paris", "Sydney"]

    fetch_and_store_weather_data(api_key, cities)

