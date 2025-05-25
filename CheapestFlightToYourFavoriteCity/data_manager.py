import requests

from flight_search import FlightSearch

url="https://api.sheety.co/e22d612cc88af32b865f71f22277c663/flightDealsNoted/prices"

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def getRows(self):
        url_get="https://api.sheety.co/e22d612cc88af32b865f71f22277c663/flightDealsNoted/prices"
        data=requests.get(url=url, auth=("mosaif5", "thispasswordismyburnersaccounts"))
        print(data.json())
        return data.json()['prices']

    def writeALLiata(self):
        listOfrows= self.getRows()
        fs = FlightSearch()
        c=2
        for row in listOfrows:
            iata=fs.get_iata_code(row['city'])
            self.updateRow(row['city'],iata,row['lowestPrice'], c)
            c=c+1

    def updateRow(self,city, iata, lprice, rnumber):
        url=f"https://api.sheety.co/e22d612cc88af32b865f71f22277c663/flightDealsNoted/prices/{rnumber}"
        body = {
            "price": {
                "city": city,
                "iataCode": iata,
                "lowestPrice": lprice,

            }
        }
        requests.put(url=url,json=body, auth=("mosaif5", "thispasswordismyburnersaccounts"))

    def writeRow(self,city,iata,lprice):
        body = {
            "price": {
                "city": city,
                "iataCode": iata,
                "lowestPrice": lprice,

            }
        }
        response = requests.post(url=url, json=body, auth=("mosaif5", "thispasswordismyburnersaccounts"))
        print(response.text)


#dt.writeRow("Paris", "PAR", 370)