import json

import requests

url = "https://restcountries.com/v3.1/name/spain"

response = requests.get(url).json()

# print(response)

print(json.dumps(response, indent=2))

print(response[0]["name"]["common"])
print(response[0]["capital"])
print(response[0]["altSpellings"])

for x in response[0]["altSpellings"]:
    print(x)
