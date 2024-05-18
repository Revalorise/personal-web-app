import requests


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
print(f"Bitcoin price in USD: {bitcoin_data['bitcoin']['usd']}")
