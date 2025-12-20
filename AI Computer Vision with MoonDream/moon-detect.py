import base64

import requests

with open("picture.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

payload = {"image_url": f"data:image/png;base64,{img_b64}", "object": "faces"}

resp = requests.post("http://localhost:2021/v1/detect", json=payload).json()
print(resp)
