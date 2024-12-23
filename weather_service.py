import os
import requests
from dotenv import load_dotenv
import ipinfo

load_dotenv()  # Load variables from .env

OWM_API_KEY = os.getenv('OWM_API_KEY')
IPINFO_TOKEN = os.getenv('IPINFO_TOKEN')

if not OWM_API_KEY:
    raise ValueError("OpenWeatherMap API key not found in .env")
if not IPINFO_TOKEN:
    raise ValueError("IPinfo token not found in .env")

def get_user_location():
    """
    Returns user's approximate location (lat, lon, city, region).
    """
    handler = ipinfo.getHandler(IPINFO_TOKEN)
    details = handler.getDetails()
    
    loc_string = details.all.get('loc', None)  # e.g. "40.7128,-74.0060"
    city = details.all.get('city', 'Unknown City')
    region = details.all.get('region', 'Unknown Region')
    
    if loc_string:
        lat, lon = loc_string.split(',')
        return {
            'lat': float(lat),
            'lon': float(lon),
            'city': city,
            'region': region
        }
    else:
        # Fallback to a default location
        return {
            'lat': 51.5074,
            'lon': 0.1278,
            'city': 'London',
            'region': 'Unknown'
        }

def get_weekly_forecast(lat, lon):
    """
    Get the 7-day forecast from OpenWeatherMap One Call API.
    """
    url = "https://api.openweathermap.org/data/2.5/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,alerts",
        "appid": OWM_API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return data.get('daily', [])

def format_forecast(daily_forecasts):
    """
    Turn the raw 7-day forecast into a list of readable strings.
    """
    formatted = []
    for i, day_data in enumerate(daily_forecasts[:7]):
        weather_desc = day_data['weather'][0]['description']
        min_temp = day_data['temp']['min']
        max_temp = day_data['temp']['max']
        day_label = f"Day {i+1}"
        
        day_string = (f"{day_label}: {weather_desc.capitalize()}, "
                      f"Temp min: {min_temp}°C, max: {max_temp}°C.")
        formatted.append(day_string)
    return formatted
