from django.db import models
from simple_history.models import HistoricalRecords

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    city_lat = models.FloatField()
    city_lon = models.FloatField()


    def __str__(self):
        return f"{self.city} - {self.timestamp}"



