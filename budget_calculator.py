import asyncio
import aiohttp
from exchange_rates_calculator import ExchangeRatesService, ExchangeRatesServiceAsync

exchange_rates_service = ExchangeRatesService()
exchange_rates_service_async = ExchangeRatesServiceAsync()

def calculate_budget_sync(budget_type: str, base_currency: str, discount: bool, data: list) -> float:
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
        return mul * sum(calculate_flights_budget_sync(base_currency, data))
    elif budget_type == "hotels":
        return mul * sum(calculate_hotels_budget_sync(base_currency, data))
    elif budget_type == "tourism":
        return mul * sum(calculate_tourism_budget_sync(base_currency, data))

    raise Exception(f"Budget type can only be one of flights, hotels or tourism, but provided {budget_type}")

def calculate_flights_budget_sync(base_currency: str, data: list):
    budgets = []
    for flight in data:
        try:
            price_obj = flight["price"]
            from_curr = price_obj["currency"]
            amount = float(price_obj["total"])
            budgets.append(exchange_rates_service.get_exchange_rate(base_currency, from_curr, amount))
        except Exception as e:
            print(e)
            continue

    return budgets

def calculate_hotels_budget_sync(base_currency: str, data: list):
    budgets = []
    for hotel in data:
        try:
            price_obj = hotel["offers"][0]["price"]
            from_curr = price_obj["currency"]
            amount = float(price_obj["total"])
            budgets.append(exchange_rates_service.get_exchange_rate(base_currency, from_curr, amount))
        except Exception as e:
            print(e)
            continue

    return budgets

def calculate_tourism_budget_sync(base_currency: str, data: list):
    budgets = []
    for tourism in data:
        try:
            price_obj = tourism["price"]
            from_curr = price_obj["currencyCode"]
            amount = float(price_obj["amount"])
            budgets.append(exchange_rates_service.get_exchange_rate(base_currency, from_curr, amount))
        except Exception as e:
            print(e)
            continue

    return budgets

async def calculate_budget_async(budget_type: str, base_currency: str, discount: bool, data: list):
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
         amounts = await asyncio.ensure_future(calculate_flights_budget_async(base_currency, data))
         return mul * sum(amounts)
    elif budget_type == "hotels":
        amounts = await asyncio.ensure_future(calculate_hotels_budget_async(base_currency, data))
        return mul * sum(amounts)
    elif budget_type == "tourism":
        amounts = await asyncio.ensure_future(calculate_tourism_budget_async(base_currency, data))
        return mul * sum(amounts)

    raise Exception(f"Budget type can only be one of flights, hotels or tourism, but provided {budget_type}")

async def calculate_flights_budget_async(base_currency: str, data: list):
    budgets = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for flight in data:
            price_obj = flight["price"]
            from_curr = price_obj["currency"]
            amount = float(price_obj["total"])
            tasks.append(asyncio.ensure_future(exchange_rates_service_async.get_exchange_rate(session, base_currency, from_curr, amount)))

        budgets = await asyncio.gather(*tasks)

    return budgets

async def calculate_hotels_budget_async(base_currency: str, data: list):
    budgets = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for hotel in data:
            price_obj = hotel["offers"][0]["price"]
            from_curr = price_obj["currency"]
            amount = float(price_obj["total"])
            tasks.append(asyncio.ensure_future(exchange_rates_service_async.get_exchange_rate(session, base_currency, from_curr, amount)))

        budgets = await asyncio.gather(*tasks)

    return budgets

async def calculate_tourism_budget_async(base_currency: str, data: list):
    budgets = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for tourism in data:
            price_obj = tourism["price"]
            from_curr = price_obj["currencyCode"]
            amount = float(price_obj["amount"])
            tasks.append(asyncio.ensure_future(exchange_rates_service_async.get_exchange_rate(session, base_currency, from_curr, amount)))

        budgets = await asyncio.gather(*tasks)

    return budgets