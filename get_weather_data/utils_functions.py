import requests


def get_weather_data(lat, lon, API_KEY):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data


def kelvin_to_celsius(kelvin):
    celsius = round(kelvin - 273.15, 2)
    return celsius


def get_air_pollution_data(lat, lon, API_KEY):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    pollution_data = response.json()
    return pollution_data
