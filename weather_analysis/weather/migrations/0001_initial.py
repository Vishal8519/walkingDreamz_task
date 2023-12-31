# Generated by Django 5.0 on 2023-12-06 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('city_lat', models.FloatField()),
                ('city_lon', models.FloatField()),
                ('historical_temperature', models.FloatField(blank=True, null=True)),
                ('historical_humidity', models.FloatField(blank=True, null=True)),
                ('historical_wind_speed', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
