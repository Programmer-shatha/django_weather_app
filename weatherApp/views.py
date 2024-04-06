from django.shortcuts import render
import requests
from datetime import datetime, timedelta
import calendar

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    api_key = "ea4046c18d24e8dcb9a8452c901e4090"
    parameters = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=parameters)
    forecast_response = requests.get(forecast_url, params=parameters)

    if response.status_code == 200 and forecast_response.status_code == 200:
        return response.json(), forecast_response.json()
    return None, None


def home(request):
    city = request.GET.get('city')
    current_weather_data, forecast_data = get_weather(city)
    
    if current_weather_data and forecast_data:
        # Extract current weather data
        weather = current_weather_data['weather'][0]['main']
        weather_description = current_weather_data['weather'][0]['description']
        city_name = current_weather_data['name']
        country = current_weather_data['sys']['country']
        wind_speed = current_weather_data['wind']['speed']
        pressure = current_weather_data['main']['pressure']
        humidity = current_weather_data['main']['humidity']
        temperature = current_weather_data['main']['temp']
        today_date = datetime.today().date()
        day_name = calendar.day_name[today_date.weekday()]
        icon = current_weather_data['weather'][0]['icon']
        
        # Extract forecast data for the next 5 days
        forecast_list = []
        today_date = datetime.today().date()
        for i in range(1, 6):  # Iterate over the next 5 days
            forecast_date = today_date + timedelta(days=i)
            forecast_list.append({
                'date': forecast_date,
                'name_day': forecast_date.strftime("%A"),
                'weather': forecast_data['list'][i]['weather'][0]['main'],
                'description': forecast_data['list'][i]['weather'][0]['description'],
                'icon': forecast_data['list'][i]['weather'][0]['icon'],
                'temperature': forecast_data['list'][i]['main']['temp']
            })
        

        context = {
            'weather': weather,
            'weather_description': weather_description,
            'city': city_name,
            'country': country,
            'wind_speed': wind_speed,
            'pressure': pressure,
            'humidity': humidity,
            'temperature': temperature,
            'icon': icon,
            'today_date': today_date,
            'day_name': day_name,
            'forecast': forecast_list,
        }
    else:
        context = {
            'error_message': "No data available for the provided city.",
        }
    
    return render(request, 'weather.html', context)












