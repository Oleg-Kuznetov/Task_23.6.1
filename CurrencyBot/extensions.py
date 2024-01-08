import requests
import json
from config import keys

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты '
                                      f'{base}!')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты!')

        if amount <= 0:
            raise APIException(f'Количество валюты не может быть меньше или '
                               f'равно 0!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym='
                         f'{base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]*amount
        total_base = round(total_base, 2)

        return total_base