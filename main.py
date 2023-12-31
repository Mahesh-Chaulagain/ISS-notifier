import time

import requests
from datetime import datetime
import smtplib

MY_EMAIL = ""   # add your email
MY_PASSWORD = ""    # add email password

MY_LAT = 27.717245
MY_LONG = 85.323959

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,    # change to 24 hour format
}


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")  # get data from the iss endpoint
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)  # sleep for 60 seconds between running the scripts
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=f"Subject:Look Up\n\nThe ISS is above you in the sky.")
