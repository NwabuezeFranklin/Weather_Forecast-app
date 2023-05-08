import datetime
import requests
from django.shortcuts import render

# Create your views here.



# https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&exclude=hourly,daily&appid=api_key
def index(request):
    api_key = '610846df89434a038984b7112d215085'
    current = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    future = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'
    
    if request.method == 'POST':
        city = request.POST['city']
        weather, future = fetch(city, api_key, current, future)
        context = {'weather': weather, 'future': future}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')
    
def fetch(city, api_key, current, future):
    response =  requests.get(current.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    future_response = requests.get(future.format(lat, lon, api_key)).json()
    print(future_response)
    
    weather_data  = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description' : response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }
    
    future_perday = []
    for daily_data in future_response['daily'][:5]:
        future_perday.append({
            'day': datetime.datetime.frontimestamp(daily_data['dt']).strftime("%A"),
            'min_temp': round(daily_data['temp'] ['min']- 273.15, 2),
            'max_temp': round(daily_data['temp'] ['max']- 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather' ][0]['icon'],     
            
        })
    return weather_data, future_perday
        
        
def tomorrow(request):
    if request.method == 'POST':
        city = request.POST['city']
        api_key = '5ndKkWpsvIMaRle8qwAGXZsiChWoZA4l'
        current = "https://api.tomorrow.io/v4/weather/realtime?location={}&apikey={}"
        response = requests.get(current.format(city, api_key)).json()
        weather, future = fetch(city, api_key, current, future)
        context = {'weather': weather, 'future': future}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')
