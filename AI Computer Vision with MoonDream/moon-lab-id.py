import base64
import json

import requests

with open("id2.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

payload = {
    "image_url": f"data:image/png;base64,{img_b64}",
    "question": "return first name, last name, date of birth and drivers license number in JSON format.  {'first':'','last':'','dob':'','dl':''}",
}

resp = requests.post("http://localhost:2021/v1/query", json=payload).json()
print(resp["answer"])

data = json.loads(resp["answer"])
print(data["first"])
print(data["last"])
print(data["dob"])
print(data["dl"])
