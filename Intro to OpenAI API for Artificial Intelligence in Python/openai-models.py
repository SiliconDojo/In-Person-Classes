import time

from openai import OpenAI

key = "YOUR API KEY"

client = OpenAI(api_key=key)


def ai(query):
    model = ["gpt-5", "gpt-5-nano", "gpt-3.5-turbo"]

    for version in model:
        speed = time.time()
        response = client.responses.create(model=version, input=query)
        speed = time.time() - speed
        print(version)
        print(f"{speed} seconds")
        print(response.output_text)
        print("---------")


while True:
    query = input("Your Query: ")
    print(query)
    ai(query)
    print("****")
