import requests
from ollama import ChatResponse, chat


def location():
    url = "http://ip-api.com/json/"
    response = requests.get(url).json()
    location = f"City: {response['city']} -- Country: {response['country']}"
    return location


def ai(query, location):
    response: ChatResponse = chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": f"""
        Answer as short as possible.
        Do not add additional information beyond the answer.
        Answer this query: {query}
        Based on this location: {location}.
        """,
            },
        ],
    )
    return response.message.content


location = location()
while True:
    query = input("Question: ")
    response = ai(query, location)
    print(response)
