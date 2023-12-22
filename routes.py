import asyncio
import datetime
from flask import Blueprint, request
from datetime import datetime
from budget_calculator import calculate_budget_sync, calculate_budget_async, calculate_flights_budget_sync, \
    calculate_hotels_budget_sync, calculate_tourism_budget_sync, calculate_hotels_budget_async, calculate_tourism_budget_async, \
    calculate_flights_budget_async

routes = Blueprint('routes', __name__)


@routes.get('/')
def health():
    return {
        "health": "up and running"
    }


@routes.post('/getItenaryCost')
async def get_itenary_cost_async():
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
            total_budget += await asyncio.ensure_future(calculate_budget_async(t, base_currency, discount, itenary_info[t]))

    return {"budget_price": total_budget, "budget_currency": base_currency}

@routes.post('/getItenaryCostSync')
def get_itenary_cost_sync():
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
            total_budget += calculate_budget_sync(t, base_currency, discount, itenary_info[t])

    return {"budget_price": total_budget, "budget_currency": base_currency}

@routes.post('/getFlightsCost')
async def get_flights_cost_async():
    input = request.json
    base_currency = input["base_currency"]
    flights = input["flights"]
    amounts = await asyncio.ensure_future(calculate_flights_budget_async(base_currency, flights))
    for (flight, amount) in zip(flights, amounts):
        flight["price"]["budget_price"] = amount
        flight["price"]["budget_currency"] = base_currency

    return {"flights": flights}

@routes.post('/getHotelsCost')
async def get_hotels_cost_async():
    input = request.json
    base_currency = input["base_currency"]
    hotels = input["hotels"]
    amounts = await asyncio.ensure_future(calculate_hotels_budget_async(base_currency, hotels))
    for (hotel, amount) in zip(hotels, amounts):
        hotel["offers"][0]["price"]["budget_price"] = amount
        hotel["offers"][0]["price"]["budget_currency"] = base_currency

    return {"hotels": hotels}

@routes.post('/getTourismCost')
async def get_tourism_cost_async():
    input = request.json
    base_currency = input["base_currency"]
    tourism = input["tourism"]
    amounts = await asyncio.ensure_future(calculate_tourism_budget_async(base_currency, tourism))
    for (t, amount) in zip(tourism, amounts):
        t["price"]["budget_price"] = amount
        t["price"]["budget_currency"] = base_currency

    return {"tourism": tourism}

@routes.post('/getFlightsCostSync')
def get_flights_cost_sync():
    input = request.json
    base_currency = input["base_currency"]
    flights = input["flights"]
    amounts = calculate_flights_budget_sync(base_currency, flights)
    for (flight, amount) in zip(flights, amounts):
        flight["price"]["budget_price"] = amount
        flight["price"]["budget_currency"] = base_currency

    return {"flights": flights}

@routes.post('/getHotelsCostSync')
def get_hotels_cost_sync():
    input = request.json
    base_currency = input["base_currency"]
    hotels = input["hotels"]
    amounts = calculate_hotels_budget_sync(base_currency, hotels)
    for (hotel, amount) in zip(hotels, amounts):
        hotel["offers"][0]["price"]["budget_price"] = amount
        hotel["offers"][0]["price"]["budget_currency"] = base_currency

    return {"hotels": hotels}

@routes.post('/getTourismCostSync')
def get_tourism_cost_sync():
    input = request.json
    base_currency = input["base_currency"]
    tourism = input["tourism"]
    amounts = calculate_tourism_budget_sync(base_currency, tourism)
    for (t, amount) in zip(tourism, amounts):
        t["price"]["budget_price"] = amount
        t["price"]["budget_currency"] = base_currency

    return {"tourism": tourism}