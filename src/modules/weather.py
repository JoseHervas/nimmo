import requests, os

def get_weather_forecasts():
    print("[+] Preparing weather data forecast...")
    api_key=os.getenv('OPEN_WEATHER_TOKEN')
    lat=os.getenv('LATITUDE')
    lon=os.getenv('LONGITUDE')
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data["daily"]
    else:
        print(response)
        return 'No se pudieron obtener los datos meteorológicos.'