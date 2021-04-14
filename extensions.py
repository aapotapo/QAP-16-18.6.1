import requests
import json
from config import EXCHANGEAPI, CRYPTOCOMPAREAPI, CRYPTOCOMPAREAPI_KEY


class APIException(RuntimeError):
    pass


class ExchangeRates:
    @staticmethod
    def rate(from_symbol, to_symbol):
        url = CRYPTOCOMPAREAPI + 'price'
        url += '?app_key=' + CRYPTOCOMPAREAPI_KEY
        url += '&fsym=' + from_symbol + '&tsyms=' + to_symbol
        response = requests.get(url)
        try:
            return json.loads(response.content)[to_symbol]
        except KeyError:
            raise RuntimeError('Не удалось получить курс обмена')

    @staticmethod
    def supported_symbols():
        response = requests.get(EXCHANGEAPI + '/currencies.json')
        if 'error' in json.loads(response.content):
            raise RuntimeError('Не удалось получить список валют')

        return json.loads(response.content)
