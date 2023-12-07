from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WeatherData
from django_filters.views import FilterView
# from .filters import WeatherDataFilter

def index(request):
    return render(request, 'index.html')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def all_weather_data(request):
    # Fetch all weather data
    all_data = WeatherData.objects.all()

    # Paginate the weather data with 10 entries per page
    paginator = Paginator(all_data, 10)
    page = request.GET.get('page', 1)

    try:
        current_page_data = paginator.page(page)
    except PageNotAnInteger:
        current_page_data = paginator.page(1)
    except EmptyPage:
        current_page_data = paginator.page(paginator.num_pages)

    # Calculate starting serial number for the page
    starting_serial_number = (current_page_data.number - 1) * paginator.per_page + 1

    context = {
        'all_weather_data': current_page_data,
        'starting_serial_number': starting_serial_number,
    }

    return render(request, 'all_weather_data.html', context)

def specific_weather_data(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        weather_data = WeatherData.objects.filter(timestamp__range=[start_date, end_date])

        return render(request, 'specific_weather_data.html', {'weather_data': weather_data})

    return render(request, 'specific_weather_data.html')

@api_view(['GET'])
def weather_data_view(request, *args, **kwargs):
    if request.method == 'GET':
       
        weather_data = WeatherData.objects.all()
        data = [
            {
                "city": entry.city,
                "temperature": entry.temperature,
                "humidity": entry.humidity,
                "wind_speed": entry.wind_speed,
                "timestamp": entry.timestamp, 
            }
            for entry in weather_data
        ]

        # Return data as JSON response
        return Response({"weather_data": data})

# from django.db.models import Avg

# def analyze_and_visualize(request):
  
#     data = WeatherData.objects.all()

    
#     avg_temperature = data.aggregate(Avg('temperature'))['temperature__avg']
#     avg_humidity = data.aggregate(Avg('humidity'))['humidity__avg']

 
#     categories = ['Temperature', 'Humidity']
#     averages = [avg_temperature, avg_humidity]

 
#     return render(request, 'analyze_and_visualize.html', {'categories': categories, 'averages': averages})


import matplotlib.pyplot as plt
from django.shortcuts import render
from django.db.models import Avg
from .models import WeatherData

def analyze_and_visualize(request):
    data = WeatherData.objects.all()

   
    avg_temperature = data.aggregate(Avg('temperature'))['temperature__avg']
    avg_humidity = data.aggregate(Avg('humidity'))['humidity__avg']


    categories = ['Temperature', 'Humidity']
    averages = [avg_temperature, avg_humidity]

   
    plt.bar(categories, averages)
    plt.xlabel('Categories')
    plt.ylabel('Averages')
    plt.title('Average Temperature and Humidity')
    plt.show()

    return render(request, 'analyze_and_visualize.html', {'categories': categories, 'averages': averages})



