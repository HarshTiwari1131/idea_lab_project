import requests
from key import key2

def get_weather_data():
    api_address = f"http://api.openweathermap.org/data/2.5/weather?q=Sonipat&appid={key2}"
    
    try:
        response = requests.get(api_address)
        response.raise_for_status()
        json_data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    return json_data

def get_weather_info():
    json_data = get_weather_data()
    if json_data:
        temp = round(json_data['main']['temp'] - 273.15, 2)  # Convert from Kelvin to Celsius
        description = json_data['weather'][0]['description']
        return {
            'temp': temp,
            'description': description
        }
    return {
        'temp': "No data",
        'description': "No data"
    }
