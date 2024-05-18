from dotenv import load_dotenv
import os
from utils_functions import kelvin_to_celsius, get_weather_data, get_air_pollution_data

load_dotenv()
API_KEY = os.getenv("WEATHER_API")


# bangkok_weather = get_weather_data(13.7563, 100.5018)
bangkok_air_pollution = get_air_pollution_data(13.7563, 100.5018, API_KEY)

## print(kelvin_to_celsius(bangkok_weather['main']['temp']))
## print(kelvin_to_celsius(bangkok_weather['main']['feels_like']))
## print(bangkok_weather['weather'][0]['main'])
## print(bangkok_weather['weather'][0]['description'])

print(bangkok_air_pollution['list'][0]['main']['aqi'])
