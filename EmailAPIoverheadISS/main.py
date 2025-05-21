import requests
from datetime import datetime
import smtplib
MY_LAT = 42.4971
# Your latitude
MY_LONG = -28.5015 # Your longitude

def inRangeLat(n):
    if (MY_LAT+5>n and MY_LAT-5<n):
        return True
    return False

def inRangeLong(n):
    if (MY_LONG+5>n and MY_LONG-5<n):
        return True
    return False


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
print(iss_latitude)
print(iss_longitude)
time_now = datetime.now()
#If the ISS is close to my current position
# and it is currently dark

if inRangeLat(iss_latitude) and inRangeLong(iss_longitude):
    if ((time_now.hour>=sunset) or (time_now.hour<=sunrise)):

        password = ""
        email = "mosaif.shaikh20@gmail.com"
        toEmail = "walkercradle@gmail.com"

        # Connection to gmail server
        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=email, password=password)

        connection.sendmail(from_addr="mosaif.shaikh20@gmail.com",
                                to_addrs="walkercradle@gmail.com",
                                msg=f"Subject:Look Up In the Sky! \n\nHey there, the ISS is right above you!")
        connection.close()
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



