import base64
import time

import cv2 as cv
import requests
from bottle import post, request, route, run, static_file


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


def ai(image, query):
    with open(image, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    payload = {"image_url": f"data:image/png;base64,{img_b64}", "object": query}

    response = requests.post("http://localhost:2021/v1/detect", json=payload).json()
    return response["objects"]


def gallery(coordinates, image):
    picture = f"""
            <div style="position:relative;
                display: inline-block; 
                border: 2px solid black; 
                height: 200px; 
                width: auto;">
            <img style="height:100%; width:auto;" src="{image}">
            """
    for image in coordinates:
        x = image["x_min"] * 100
        width = (image["x_max"] - image["x_min"]) * 100
        y = image["y_min"] * 100
        height = (image["y_max"] - image["y_min"]) * 100

        picture += f"""
            <div style="position: absolute;
                border: 2px solid lime;
                box-sizing: border-box;
                left:{x}%; 
                top:{y}%; 
                width:{width}%; 
                height:{height}%;">
            </div>
            """
    picture += "</div>"

    return picture


@route("/", method=["GET", "POST"])
def index():
    query = request.forms.get("find")
    form = """
            <form method="post" action="/">
                Find: <input type="text" name="find">
                <br>
                <input type="submit">
            </form>
            """
    if query != None:
        print(query)
        image = camera()
        coordinates = ai(image, query)
        picture = gallery(coordinates, image)

        page = f"""
                <h1>Web App</h1>
                {picture}
                <br>
                {form}
                <br>
                {coordinates}
                """
    else:
        page = f"""
                <h1>Web App</h1>
                <br>
                {form}
                """
    return page


@route("/<filename:path>")
def serve_static(filename):
    return static_file(filename, root="./")


run(host="127.0.0.1", port=8080)
