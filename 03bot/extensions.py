import requests
import json
from config import keys, API_KEY

class ConvertionException(Exception):
    pass

class get_price():
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Вы пытаетесь коверировать валюту {base} саму в себя.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Ощибка перевода в число [{amount}].')
        #Из-за жадности буржуйского api находим курсы через курс к евро каждой из валют
        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&symbols={quote_ticker},{base_ticker}&format=1')
        resp = json.loads(r.content)
        itog = float(resp['rates'][base_ticker])/float(resp['rates'][quote_ticker])*amount
        itog = round(itog, 3)
        return itog