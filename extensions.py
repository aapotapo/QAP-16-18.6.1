import requests
import json
from config import EXCHANGEAPI, CRYPTOCOMPAREAPI, CRYPTOCOMPAREAPI_KEY


class APIException(RuntimeError):
    pass


class ExchangeRates:
    @staticmethod
    def get_price(base, quote, amount):
        url = CRYPTOCOMPAREAPI + 'price'
        url += '?app_key=' + CRYPTOCOMPAREAPI_KEY
        url += '&fsym=' + base + '&tsyms=' + quote
        response = requests.get(url)
        try:
            rate = json.loads(response.content)[quote]
            return round(float(amount) * rate, 2)
        except KeyError:
            raise RuntimeError('Не удалось получить курс обмена')


    @staticmethod
    def supported_symbols():
        response = requests.get(EXCHANGEAPI + '/currencies.json')
        if 'error' in json.loads(response.content):
            raise RuntimeError('Не удалось получить список валют')

        return json.loads(response.content)
