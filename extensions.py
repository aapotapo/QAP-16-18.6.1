import requests
import json
from config import EXCHANGEAPI, EXCHANGEAPI_KEY


class APIException(RuntimeError):
    pass


class ExchangeRates:
    @staticmethod
    def rate(from_symbol, to_symbol):
        url = EXCHANGEAPI + 'latest.json'
        url += '?app_id=' + EXCHANGEAPI_KEY
        url += '&base=' + from_symbol + '&symbols=' + to_symbol
        response = requests.get(url)
        if 'error' in json.loads(response.content):
            raise RuntimeError(f'Не удалось получить курс обмена')
        return json.loads(response.content)['rates'][to_symbol]

    @staticmethod
    def supported_symbols():
        response = requests.get(EXCHANGEAPI + '/currencies.json')
        if 'error' in json.loads(response.content):
            raise RuntimeError(f'Не удалось получить список валют')

        return json.loads(response.content)
