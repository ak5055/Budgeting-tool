from exchange_rates_calculator import ExchangeRatesService

exchange_rates_service = ExchangeRatesService()

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
            total_budget += exchange_rates_service.get_exchange_rate(base_currency, from_curr, amount)
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
            total_budget += exchange_rates_service.get_exchange_rate(base_currency, from_curr, amount)
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
            total_budget += exchange_rates_service.get_exchange_rate(base_currency, from_curr, amount)
        except Exception as e:
            print(e)
            continue

    return total_budget
