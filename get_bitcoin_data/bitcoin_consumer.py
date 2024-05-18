from kafka import KafkaConsumer
import json

# Getting the data as JSON
consumer = KafkaConsumer('btc-price',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda x: json.loads(x.decode('ascii')))


for message in consumer:
    price = message.value
    print('Bitcoin price: ' + str(price))
