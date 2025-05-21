import requests

OMW_Endpoint="https://api.openweathermap.org/data/2.5/forecast"
api_key=""

weather_params={
    "lat":43.604652 ,
    "lon":1.444209,
    "appid": api_key,
    "cnt":4,
}

response=requests.get(OMW_Endpoint, params=weather_params)
response.raise_for_status()
weather_data=response.json()
# print(weather_data["list"][0]["weather"][0]["id"])
# print(len(weather_data["list"]))
rain=False
for i in range(len(weather_data["list"])):
    for j in range(len(weather_data["list"][i]["weather"])):
        if weather_data["list"][i]["weather"][j]["id"]<700:
            rain=True
            break
    if (rain):
        break
print(f"Your coordinates are Latitude: {weather_params['lat']} and Longitude: {weather_params['lon']}")
if rain:
    print("There are chances of rain in the next 24 hours. Get Your Umbrella Cuz.")
else:
    print("There isnt any forecast for rain at your coordinates in the next 24 hours")
