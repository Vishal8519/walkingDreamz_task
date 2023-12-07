from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import WeatherData

class WeatherDataViewTests(TestCase):

    def setUp(self):
        self.weather_data = WeatherData.objects.create(
            city='TestCity',
            temperature=25.0,
            humidity=60,
            wind_speed=5.0,
            city_lat = 0.00,
            city_lon = 10.00,
            timestamp=timezone.now()
        )

    def test_specific_weather_data_view(self):
        response = self.client.get(reverse('specific_weather_data'))
        self.assertEqual(response.status_code, 200)

    def test_specific_weather_data_post_request(self):
       
        start_date = timezone.now().strftime('%Y-%m-%d')
        end_date = (timezone.now() + timezone.timedelta(days=1)).strftime('%Y-%m-%d')

        response = self.client.post(reverse('specific_weather_data'), {'start_date': start_date, 'end_date': end_date})
        self.assertEqual(response.status_code, 200)

        self.assertIn('weather_data', response.context)
   
        response = self.client.post(reverse('specific_weather_data'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('specific_weather_data'))
        self.assertEqual(response.status_code, 200)
