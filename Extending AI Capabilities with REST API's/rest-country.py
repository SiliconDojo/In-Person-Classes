import requests
from ollama import ChatResponse, chat


def location():
    url = "http://ip-api.com/json/"
    response = requests.get(url).json()
    country = response["country"]
    return country


def country_api(country):
    url = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(url).json()
    return response


def ai(query, location):
    response: ChatResponse = chat(
        model="gpt-oss",
        messages=[
            {
                "role": "user",
                "content": f"""
        1. Answer as short as possible.
        2. Only answer the question.
        3. Answer this query: {query}
        4. Provide the Value from the key/value pairs in this JSON: {location}.
        5. Only provide the Value from the Data provided.
        """,
            },
        ],
    )
    return response.message.content


country = location()
country_data = country_api(country)

while True:
    query = input("Question: ")
    response = ai(query, country_data)
    print(response)
