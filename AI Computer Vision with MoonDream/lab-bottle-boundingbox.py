import base64
import os

import requests
from bottle import post, request, route, run, static_file

folder = "pic"
files = os.listdir(folder)


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
    gallery_html = ""
    if query != None:
        for x in files:
            image = os.path.join("pic", x)
            coordinates = ai(image, query)
            picture = gallery(coordinates, image)
            gallery_html += picture

        page = f"""
                <h1>Web App</h1>
                {form}
                <br>
                {gallery_html}
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
