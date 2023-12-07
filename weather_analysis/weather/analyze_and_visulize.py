import asyncio
import httpx
import matplotlib.pyplot as plt
from datetime import datetime
from django.shortcuts import render
from django.db.models import Avg
from configparser import ConfigParser
from pathlib import Path
import os

from weather_analysis.settings import *

API_KEY = API_KEY

CITIES = ["London", "New York", "Tokyo", "Paris", "Sydney"]

async def fetch_weather_data_async(api_key, city, session):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

    async with session.get(url) as response:
        return await response.json()

async def fetch_all_weather_data(api_key, cities):
    async with httpx.AsyncClient() as client:
        tasks = [fetch_weather_data_async(api_key, city, client) for city in cities]
        
        return await asyncio.gather(*tasks)

def fetch_weather_data(api_key, city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = httpx.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def analyze_and_visualize(request):
 
    api_key = API_KEY
    cities = CITIES
    async_start_time = datetime.now()
  
    async_data = asyncio.run(fetch_all_weather_data(api_key, cities))
    async_end_time = datetime.now()
    async_duration = async_end_time - async_start_time
   
    sync_start_time = datetime.now()
    sync_data = [fetch_weather_data(api_key, city) for city in cities]
    sync_end_time = datetime.now()
    sync_duration = sync_end_time - sync_start_time

    async_start_time = datetime.now()
    async_data = asyncio.run(fetch_all_weather_data(api_key, cities))
    async_end_time = datetime.now()
    async_duration = async_end_time - async_start_time

    sync_temperatures = [data['main']['temp'] for data in sync_data]
    async_temperatures = [data['main']['temp'] for data in async_data]

   
    avg_sync_temperature = sum(sync_temperatures) / len(sync_temperatures)
    avg_async_temperature = sum(async_temperatures) / len(async_temperatures)

    labels = ['Synchronous', 'Asynchronous']
    averages = [avg_sync_temperature, avg_async_temperature]

    plt.bar(labels, averages)
    plt.xlabel('Request Type')
    plt.ylabel('Average Temperature (°C)')
    plt.title('Average Temperature Comparison')
    plt.show()

   
    return render(request, 'analyze_and_visualize.html')

