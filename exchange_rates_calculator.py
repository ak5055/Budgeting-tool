import csv
import json
import requests
import warnings
from constants import GET_EXCHANGE_RATE_BASE_URL, EXCHANGE_RATES_FALLBACK_FILE


class ExchangeRatesService:
    def __init__(self):
        self.fallback_file = EXCHANGE_RATES_FALLBACK_FILE
        self.exchange_rates_url = GET_EXCHANGE_RATE_BASE_URL
        self.fallback_exchange_rates = {}
        self.preprocess_fallback_data()

    def preprocess_fallback_data(self):
        with open(self.fallback_file, mode='r') as file:
            exchange_rates_file = csv.DictReader(file)
            for row in exchange_rates_file:
                currency = row['currency']
                value = float(row['value'])
                self.fallback_exchange_rates[currency] = value

    def get_exchange_rate_from_api(self, base_currency: str, from_currency: str, amount: float) -> float:
        headers = {'token': 'secret', 'content-type': 'application/json'}
        body = {'from_curr': from_currency, 'to_curr': base_currency, 'amount': amount}
        url = f'{GET_EXCHANGE_RATE_BASE_URL}/getRate'
        resp = requests.post(url, data=json.dumps(body), headers=headers).json()
        return float(resp["amount"])

    def get_fallback_exchange_rate(self, base_currency: str, from_currency: str, amount: float) -> float:
        '''
            Exchange rate fallback behavior if exchange rates api is not working properly
        '''
        return (self.fallback_exchange_rates[base_currency] / self.fallback_exchange_rates[from_currency]) * amount

    def get_exchange_rate(self, base_currency: str, from_currency: str, amount: float) -> float:
        try:
            return self.get_exchange_rate_from_api(base_currency, from_currency, amount)
        except Exception as e:
            warnings.warn(f"The exchange rates api failed because of the following exception: {e}. "
                          f"Falling back to getting exchange rates from static file instead.")
            return self.get_fallback_exchange_rate(base_currency, from_currency, amount)
