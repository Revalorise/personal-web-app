from dotenv import load_dotenv
from os import environ

load_dotenv()

API_KEY = environ.get("WEATHER_API")
