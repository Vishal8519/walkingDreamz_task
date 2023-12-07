import os
import django
import asyncio
import httpx
from asgiref.sync import sync_to_async
from django.db import models
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_analysis.settings')
django.setup()
from weather.models import WeatherData
import time
import datetime

@sync_to_async
def create_weather_data(city, temperature, humidity, wind_speed, timestamp):
    WeatherData.objects.create(
        city=city,
        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
        timestamp=timestamp
    )

async def fetch_city_lat_lon(api_key, city):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            print(f'Error: No data found for the city {city}')
            return None, None

async def fetch_historical_weather_data(api_key, city, start_date, end_date):
    lat, lon = await fetch_city_lat_lon(api_key, city)

    if lat is not None and lon is not None:
        base_url = 'https://history.openweathermap.org/data/3.0/history/timemachine'
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())

        url = f'{base_url}?lat={lat}&lon={lon}&dt={start_timestamp}&appid={api_key}'

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()

            print(data)

            for entry in data:
                temperature = entry['main']['temp']
                humidity = entry['main']['humidity']
                wind_speed = entry['wind']['speed']
                timestamp = datetime.datetime.utcfromtimestamp(entry['dt'])

                await create_weather_data(city, temperature, humidity, wind_speed, timestamp)

                print(f'Successfully fetched and stored historical data for {city} on {timestamp}.')

async def main(api_key, cities):
    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime(2022, 12, 31)

    tasks = [
        fetch_historical_weather_data(api_key, city, start_date, end_date)
        for city in cities
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    api_key = settings.API_KEY
    cities = ["London", "New York", "Tokyo", "Paris", "Sydney"]
    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime(2022, 12, 31)

    
    start_time_async = time.time()
    asyncio.run(main(api_key, cities))
    end_time_async = time.time()
    async_duration = end_time_async - start_time_async

  
    start_time_sync = time.time()
    for city in cities:
        asyncio.run(fetch_historical_weather_data(api_key, city, start_date, end_date))
    end_time_sync = time.time()
    sync_duration = end_time_sync - start_time_sync

    print(f"Time taken for asynchronous requests: {async_duration} seconds")
    print(f"Time taken for synchronous requests: {sync_duration} seconds")
