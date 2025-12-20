import base64
import os
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
        "question": """
        if there a person in this image in orange clothing answer 'orange'.
        If there is a person in the image without orange clothing answer 'person'.
        If there is no person answer 'empty'
        """,
    }

    resp = requests.post("http://localhost:2021/v1/query", json=payload).json()
    return resp["answer"]


while True:
    image = camera()
    response = ai(image)
    print(response)
    if "person" in response:
        os.system("afplay alert.mp3")
    elif "orange" in response:
        os.system("afplay welcome.mp3")
    else:
        os.system("afplay crickets.wav")

    print(response)
    time.sleep(1)
