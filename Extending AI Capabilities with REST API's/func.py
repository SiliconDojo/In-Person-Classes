import datetime

import requests


def hello():
    message = "yo dude!"
    return message


def bye():
    message = "see ya buddy"
    return message


def clock():
    current_time = datetime.datetime.now()
    return current_time


def location():
    url = "http://ip-api.com/json/"
    response = requests.get(url).json()
    location = {"lat": "", "lon": ""}
    location["lat"] = response["lat"]
    location["lon"] = response["lon"]
    return location


def weather():
    url = "http://ip-api.com/json/"
    response = requests.get(url).json()
    lat = response["lat"]
    lon = response["lon"]

    key = "YOUR API KEY"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=imperial"
    response = requests.get(url).json()
    return response
