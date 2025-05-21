import requests
import datetime as dt
APP_ID="eb583490"
API_KEY=""

params={
    "query":input("Please input the exercise you did today: "),
}
headers={
    'Content-Type': 'application/json',
    'x-app-id':APP_ID ,
    'x-app-key':API_KEY,
}

today=dt.datetime.today()
print(today)
nutrition_endpoint="https://trackapi.nutritionix.com/v2/natural/exercise"
response=requests.post(url=nutrition_endpoint, headers=headers, json=params)
data=response.json()
print(data)
sheety_Endpoint="https://api.sheety.co/0a05621a07c9e96a6dd34907b8a257f2/workoutTracking/workouts"

for exercise in data['exercises']:
    body = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%H:%M:%S"),
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
        }
    }
    print(body)
    response=requests.post(url=sheety_Endpoint,json=body, auth=("mosaif5", ""))
    print(response.text)

