from datetime import datetime

import requests
API_KEY = "hidden"
API_SECRET = "hidden"
class FlightSearch:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret =API_SECRET
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = "https://api.amadeus.com/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_iata_code(self, city):
        url = "https://api.amadeus.com/v1/reference-data/locations/cities"
        city = city
        params = {
            "keyword": city,
            "max": 2,
            "include": "AIRPORTS"
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data=response.json()
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}.")
            return "Not Found"

        return code

    def get_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        FLIGHT_ENDPOINT = "https://api.amadeus.com/v2/shopping/flight-offers"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "false",
            "currencyCode": "KWD",
            "max": "30",
            "maxPrice":90,
        }

        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"get_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None
        return response.json()


# fs = FlightSearch()
# print(fs.get_access_token())
# print(fs.get_flights(
#      "KWI",
#      "AUH",
#      datetime.strptime("2025-06-27", "%Y-%m-%d"),
#      datetime.strptime("2025-07-04", "%Y-%m-%d")
#  ))
# print(fs.get_iata_code("Abu Dhabi"))
#print(fs.get_iata_code())
