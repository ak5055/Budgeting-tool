# budgeting-tool
This is a microservice for calculating budgets relating to our trip planner application.
(Below functions also have a synchronous version in addition to the
asynchronous version):
<ul>
<li>POST /getItenaryCost: Calculates the total itinerary cost in a base currency
taking into consideration the flights, hotels and the tours and activities
booked. It also provides 10 percent discount if user’s date of birth is on the
same month as the booking date. 
  <ul>
  <li>  Body <ul>
    <li>Itenary: dictionary of booked flights, hotels, tours and
activities</li>
    <li>Base_currency: string. The base currency to show the cost</li>
    <li>Dob: string. Date of birth of the user id. (This is fetched from
the user microservice and this function is not called directly).</li> </ul></li> </ul> </li>

<li>POST /getFlightsCost: Calculates the cost to book each of the flights.
(Return value is a list consisting of each of the costs)
  <ul>
  <li>  Body <ul>
    <li>Base_currency: string. The base currency to show the cost</li>
    <li>Flights: The list of flights to calculate cost in base currency.</li> </ul></li> </ul> </li>

<li>POST /getHotelsCost: Calculates the cost to book each of the hotels.
(Return value is a list consisting of each of the costs) 
  <ul>
  <li>  Body <ul>
    <li>Base_currency: string. The base currency to show the cost</li>
    <li>Hotels: The list of hotels to calculate cost in base currency.</li> </ul></li> </ul> </li>

  <li>/getTourismCost: Calculates the cost to book each of the tourism
costs. (Return value is a list consisting of each of the costs). 
  <ul>
  <li>  Body <ul>
    <li>Base_currency: string. The base currency to show the cost</li>
    </ul></li> </ul> </li>
