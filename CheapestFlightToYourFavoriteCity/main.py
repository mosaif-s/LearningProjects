
import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager


data_manager = DataManager()
sheet_data = data_manager.getRows()
flight_search = FlightSearch()
nmanage=NotificationManager()

# Set your origin airport
#data_manager.writeALLiata()

ORIGIN_CITY_IATA = "KWI"
DESTINATION_CITY_IATA = "AUH"

tomorrow = datetime.now() + timedelta(days=1)
TWO_months_later = datetime.now() + timedelta(days=60)

cheapest_overall = None

current_departure = tomorrow
while current_departure <= TWO_months_later - timedelta(days=7):  # ensure return stays in range
    return_date = current_departure + timedelta(days=7)

    print(f"Searching: {current_departure.date()} → {return_date.date()}")

    flight_data = flight_search.get_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=DESTINATION_CITY_IATA,
        from_time=current_departure,
        to_time=return_date
    )

    cheapest = find_cheapest_flight(flight_data)

    if cheapest.price != "N/A":
        if cheapest_overall is None or float(cheapest.price) < float(cheapest_overall.price):
            cheapest_overall = cheapest
            print(f"🟢 New cheapest: {cheapest.price} KD: ({cheapest.out_date} → {cheapest.return_date})")

    #time.sleep(2)
    current_departure += timedelta(days=1)

if cheapest_overall:
    print("\n✅ Cheapest round-trip from KWI to AUH in next 2 months:")
    print(f"💸 Price: KD {cheapest_overall.price+8}")
    print(f"🛫 Departure: {cheapest_overall.out_date}")
    print(f"🛬 Return: {cheapest_overall.return_date}")
    nmanage.sendMessage(f"✅ Cheapest round-trip from KWI to AUH in next 2 months: \n"
                        f"💸 Price: KD {cheapest_overall.price+8}\n"
                        f"🛫 Departure: {cheapest_overall.out_date}\n"
                        f"🛬 Return: {cheapest_overall.return_date}")
else:
    print("❌ No flights found.")

