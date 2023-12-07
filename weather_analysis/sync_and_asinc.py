import os
import django
import asyncio
import httpx
import time
import matplotlib.pyplot as plt
from asgiref.sync import sync_to_async
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_analysis.settings')
django.setup()
from weather.models import WeatherData

@sync_to_async
def create_weather_data(city, temperature, humidity, wind_speed, lat, lon):
    WeatherData.objects.create(
        city=city,
        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
        city_lon=lon,
        city_lat=lat,
    )

async def fetch_weather_data(api_key, city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        lat = data['coord']['lat']
        lon = data['coord']['lon']

        await create_weather_data(city, temperature, humidity, wind_speed, lat, lon)
        print(f'Successfully fetched and stored data for {city}.')

async def main(api_key, cities):
    tasks = [fetch_weather_data(api_key, city) for city in cities]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    api_key = settings.API_KEY
    cities = ["London", "New York", "Tokyo", "Paris", "Sydney"]

    start_time_async = time.time()
    asyncio.run(main(api_key, cities))
    end_time_async = time.time()
    async_duration = end_time_async - start_time_async

    start_time_sync = time.time()
    for city in cities:
        asyncio.run(fetch_weather_data(api_key, city))
    end_time_sync = time.time()
    sync_duration = end_time_sync - start_time_sync

    print(f"Time taken for asynchronous requests: {async_duration} seconds")
    print(f"Time taken for synchronous requests: {sync_duration} seconds")

    labels = ['Asynchronous', 'Synchronous']
    durations = [async_duration, sync_duration]

    plt.bar(labels, durations)
    plt.xlabel('Request Type')
    plt.ylabel('Time (seconds)')
    plt.title('Time Taken for API Requests')
    plt.show()

