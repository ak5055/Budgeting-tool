import datetime
from flask import Blueprint, request
from datetime import datetime
from budget_calculator import calculate_budget, calculate_tourism_budget, calculate_flights_budget, calculate_hotels_budget
routes = Blueprint('routes', __name__)


@routes.get('/')
def health():
    return {
        "health": "up and running"
    }


@routes.post('/getItenaryCost')
def get_itenary_cost():
    input = request.json

    dob = input["dob"]
    base_currency = input["base_currency"]
    itenary_info = input["itenary"]
    types = ["flights", "hotels", "tourism"]
    discount = False
    if datetime.strptime(dob, "%Y-%m-%d").month == datetime.now().month:
        discount = True

    total_budget = 0
    for t in types:
        if t in itenary_info:
            total_budget += calculate_budget(t, base_currency, discount, itenary_info[t])

    return {"budget_price": total_budget, "budget_currency": base_currency}

@routes.post('/getFlightsCost')
def get_flights_cost():
    input = request.json
    base_currency = input["base_currency"]
    flights = input["flights"]
    costs = {}
    for flight in flights:
        flight["price"]["budget_price"] = calculate_flights_budget(base_currency, [flight])
        flight["price"]["budget_currency"] = base_currency

    return {"flights": flights}

@routes.post('/getHotelsCost')
def get_hotels_cost():
    input = request.json
    base_currency = input["base_currency"]
    hotels = input["hotels"]
    costs = {}
    for hotel in hotels:
        hotel["offers"][0]["price"]["budget_price"] = calculate_hotels_budget(base_currency, [hotel])
        hotel["offers"][0]["price"]["budget_currency"] = base_currency

    return {"hotels": hotels}

@routes.post('/getTourismCost')
def get_tourism_cost():
    input = request.json
    base_currency = input["base_currency"]
    tourism = input["tourism"]
    for t in tourism:
        t["price"]["budget_price"] = calculate_tourism_budget(base_currency, [t])
        t["price"]["budget_currency"] = base_currency

    return {"tourism": tourism}