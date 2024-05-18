from time import sleep
from utils_functions import get_weather_data, get_air_pollution_data
from kafka import KafkaProducer
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY = os.getenv("WEATHER_API")

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('ascii'))


while True:
    sleep(10)
    bangkok_weather = get_weather_data(13.7563, 100.5018, API_KEY)
    print("Weather fetched")
    producer.send('bangkok_temperature', value=bangkok_weather)
    print("Weather data sent to consumer")

    bangkok_pollution = get_air_pollution_data(13.7563, 100.5018, API_KEY)
    print("Air pollution fetched")
    producer.send('bangkok_pollution', value=bangkok_pollution)
    print("Air pollution data sent to consumer")
