import json
import requests
from constants import GET_EXCHANGE_RATE_BASE_URL

def calculate_budget(budget_type: str, base_currency: str, discount: bool, data: list) -> float:
    '''

    :param budget_type:
    :param base_currency:
    :param discount: If discount applied true, then take 90% of answer
    :param data:
    :return:
    '''
    mul = 1.0
    if discount:
        mul = 0.9

    if budget_type == "flights":
        return mul * calculate_flights_budget(base_currency, data)
    elif budget_type == "hotels":
        return mul * calculate_hotels_budget(base_currency, data)
    elif budget_type == "tourism":
        return mul * calculate_tourism_budget(base_currency, data)

    raise Exception(f"Budget type can only be one of flights, hotels or tourism, but provided {budget_type}")

def calculate_flights_budget(base_currency: str, data: list) -> float:
    total_budget = 0
    for flight in data:
        try:
            price_obj = flight["price"]
            from_curr = price_obj["currency"]
            amount = float(price_obj["total"])
            total_budget += get_exchange_rate(base_currency, from_curr, amount)
        except Exception as e:
            print(e)
            continue

    return total_budget

def calculate_hotels_budget(base_currency: str, data: list) -> float:
    total_budget = 0
    for hotel in data:
        try:
            price_obj = hotel["offers"][0]["price"]
            from_curr = price_obj["currency"]
            amount = float(price_obj["total"])
            total_budget += get_exchange_rate(base_currency, from_curr, amount)
        except Exception as e:
            print(e)
            continue

    return total_budget

def calculate_tourism_budget(base_currency: str, data: list) -> float:
    total_budget = 0
    for tourism in data:
        try:
            price_obj = tourism["price"]
            from_curr = price_obj["currencyCode"]
            amount = float(price_obj["amount"])
            total_budget += get_exchange_rate(base_currency, from_curr, amount)
        except Exception as e:
            print(e)
            continue

    return total_budget

def get_exchange_rate(base_currency, from_currency, amount):
    headers = {'token': 'secret', 'content-type': 'application/json'}
    body = {'from_curr': from_currency, 'to_curr': base_currency, 'amount': amount}
    url = f'{GET_EXCHANGE_RATE_BASE_URL}/getRate'
    resp = requests.post(url, data=json.dumps(body), headers=headers).json()
    return float(resp["amount"])



