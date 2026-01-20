import base64
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


def ai(query, image):
    with open(image, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    payload = {"image_url": f"data:image/png;base64,{img_b64}", "question": query}

    resp = requests.post("http://localhost:2021/v1/query", json=payload).json()
    return resp["answer"]


while True:
    query = input("Question: ")
    image = camera()
    response = ai(query, image)
    print(response)
