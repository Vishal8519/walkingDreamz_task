from django.shortcuts import render
from django.views import View
from .models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.views import FilterView
import matplotlib.pyplot as plt
from django.db.models import Avg


def index(request):
    return render(request, 'index.html')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def all_weather_data(request):
    all_data = WeatherData.objects.all()
    paginator = Paginator(all_data, 10)
    page = request.GET.get('page', 1)

    try:
        current_page_data = paginator.page(page)
    except PageNotAnInteger:
        current_page_data = paginator.page(1)
    except EmptyPage:
        current_page_data = paginator.page(paginator.num_pages)
    starting_serial_number = (current_page_data.number - 1) * paginator.per_page + 1

    context = {
        'all_weather_data': current_page_data,
        'starting_serial_number': starting_serial_number,
    }

    return render(request, 'all_weather_data.html', context)



def specific_weather_data(request):
    all_weather_data = WeatherData.objects.all()
    weather_data = all_weather_data

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        city = request.POST.get('city')

        filter_conditions = {}

        if start_date:
            filter_conditions['timestamp__gte'] = start_date
        if end_date:
            filter_conditions['timestamp__lte'] = end_date
        if city:
            filter_conditions['city__icontains'] = city

        weather_data = all_weather_data.filter(**filter_conditions)

    return render(request, 'specific_weather_data.html', {'weather_data': weather_data})


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
        return Response({"weather_data": data})



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



