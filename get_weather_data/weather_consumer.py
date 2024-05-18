import json
from kafka import KafkaConsumer
from utils_functions import kelvin_to_celsius


weather_consumer = KafkaConsumer('bangkok_temperature', bootstrap_servers=['localhost:9092'],
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')))


pollution_consumer = KafkaConsumer('bangkok_pollution', bootstrap_servers=['localhost:9092'],
                                   value_deserializer=lambda m: json.loads(m.decode('ascii')))


air_quality = {
    1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very poor", 6: "Hazardous"
}


for message in weather_consumer:
    temperature_data = message.value
    print(f"Current bangkok temperature is: {kelvin_to_celsius(temperature_data['main']['temp'])} °C")

for message in pollution_consumer:
    print("Bangkok air pollution fetched")
    pollution_data = message.value
    print(f"Current bangkok air quality is: {air_quality[pollution_data['list'][0]['main']['aqi']]}")
