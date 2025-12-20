import base64
import json
import time

import cv2 as cv
import requests
from bottle import post, request, route, run, static_file


def camera():
    cam = cv.VideoCapture(0)
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


@route("/", method=["GET", "POST"])
def index():
    trigger = request.query.get("take_picture")
    if trigger == "yes":
        image = camera()
        response = ai(image)
        print(response)

        data = json.loads(response)

        page = f"""
                <h1>Web App</h1>
                <h2><a href="/?take_picture=yes">Take Picture</a></h2>
                <img style="height:200px;width:auto;" src="{image}">
                <br>
                {response}
                <br>
                <form>
                First: <input type="text" name="first" value="{data['first']}">
                <br>
                Last: <input type="text" name="last" value="{data['last']}">
                <br>
                DOB: <input type="text" name="dob" value="{data['dob']}">
                <br>
                DL#: <input type="text" name="dl" value="{data['dl']}">
                </form>
                """
    else:
        page = """
                <h1>Web App</h1>
                <h2><a href="/?take_picture=yes">Take Picture</a></h2>
                """

    return page


@route("/<filename:path>")
def serve_static(filename):
    return static_file(filename, root="./")


run(host="127.0.0.1", port=8080)
