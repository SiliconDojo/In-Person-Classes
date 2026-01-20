import requests
from ollama import ChatResponse, chat


def location():
    url = "http://ip-api.com/json/"
    response = requests.get(url).json()
    location = {"lat": "", "lon": ""}
    location["lat"] = response["lat"]
    location["lon"] = response["lon"]
    return location


def weather(lat, lon):
    key = "YOUR API KEY"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=imperial"
    response = requests.get(url).json()
    return response


def ai(query, location):
    response: ChatResponse = chat(
        model="gpt-oss",
        messages=[
            {
                "role": "user",
                "content": f"""
        Answer as short as possible.
        Do not add additional information beyond the answer.
        Answer this query: {query}
        Based on this information: {location}.
        """,
            },
        ],
    )
    return response.message.content


location = location()
weather = weather(location["lat"], location["lon"])

while True:
    query = input("Question: ")
    response = ai(query, weather)
    print(response)
