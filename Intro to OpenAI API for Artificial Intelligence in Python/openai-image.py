import time

import requests
from openai import OpenAI

key = "YOUR API KEY"

client = OpenAI(api_key=key)

result = client.images.generate(model="dall-e-3", prompt="A person riding a cat", size="1024x1024")

image_url = result.data[0].url

print(result)
print("****")
print(result.data[0].revised_prompt)
print("****")
print(image_url)

img_data = requests.get(image_url).content
filename = f"{int(time.time())}.png"

with open(filename, "wb") as handler:
    handler.write(img_data)
