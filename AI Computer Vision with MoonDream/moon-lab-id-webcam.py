import base64
import json
import time

import cv2 as cv
import requests


def camera():
    cam = cv.VideoCapture(1)
    time.sleep(0.5)
    ret, frame = cam.read()
    image = "captured_image.png"

    if ret:
        cv.imwrite(image, frame)
    else:
        print("Failed to capture image.")

    cam.release()
    return image


def ai(image):
    with open(image, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    payload = {
        "image_url": f"data:image/png;base64,{img_b64}",
        "question": "return first name, last name, date of birth and drivers license number in JSON format.  {'first':'','last':'','dob':'','dl':''}",
    }

    resp = requests.post("http://localhost:2021/v1/query", json=payload).json()
    return resp["answer"]


image = camera()
response = ai(image)
print(response)

data = json.loads(response)
print(data["first"])
print(data["last"])
print(data["dob"])
print(data["dl"])
