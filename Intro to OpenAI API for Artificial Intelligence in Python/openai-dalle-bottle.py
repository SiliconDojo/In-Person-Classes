import time

import requests
from bottle import post, request, route, run
from openai import OpenAI

injection = "Add some pasta"


def ai(query):
    key = "YOUR API KEY"

    client = OpenAI(api_key=key)

    result = client.images.generate(model="dall-e-3", prompt=query, size="1024x1024")

    image_url = result.data[0].url
    revised_prompt = result.data[0].revised_prompt

    return image_url, revised_prompt


def download(image_url):
    img_data = requests.get(image_url).content
    filename = f"{int(time.time())}.png"

    with open(filename, "wb") as handler:
        handler.write(img_data)

    return filename


def gallery():
    with open("gallery.csv", "r") as file:
        pictures = file.readlines()
    gallery = ""
    for image in pictures:
        item = image.split("|")
        gallery += f"""
                    <div style="display:inline-block; width:200px; height:auto;">
                        <img style="width:100%; height:auto;" src="{item[0]}">
                        <p>{item[1]}<p>
                    </div>
                    """

    return gallery


@route("/", method=["GET", "POST"])
def index():
    query = request.forms.get("query")

    if query:
        query_full = f"{injection} -- {query}"
        response = ai(query_full)
        with open("gallery.csv", "a") as file:
            file.write(f"{response[0]}|{response[1]}\n")
    else:
        response = "***"

    pic_gallery = gallery()

    page = f"""
            <h1>Web App</h1>
            <form action="/" method="post">
                Create an Image: <input type="text" name="query">
                <br>
                <input type="submit">
            </form>
            <strong>{query}</strong><br>
            {response}<br>
            {pic_gallery}
            """
    return page


run(host="localhost", port=8080)
