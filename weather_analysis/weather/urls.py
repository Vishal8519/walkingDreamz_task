from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('weather-data/', weather_data_view, name='weather_data'),
    path('analyze_and_visualize/', analyze_and_visualize, name='analyze_and_visualize'),
    path('all-weather-data/', all_weather_data, name='all_weather_data'),
    path('specific-weather-data/', specific_weather_data, name='specific_weather_data'),
]


