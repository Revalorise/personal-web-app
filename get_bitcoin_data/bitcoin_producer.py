from kafka import KafkaProducer
from time import sleep
import requests
import json


# Coinbase API endpoint
url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'

# Producing as JSON
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('ascii'))


def get_bitcoin_data():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


bitcoin_data = get_bitcoin_data()

while True:
    sleep(10)
    price = ((requests.get(url)).json())
    print("Price fetched")
    producer.send('btc-price', bitcoin_data['bitcoin']['usd'])
    print("Price sent to consumer")
