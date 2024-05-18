import requests
from dotenv import load_dotenv
from os import environ

load_dotenv()

API_KEY = environ.get("WEATHER_API")


def call_url(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
