import sqlite3
import time

import requests
from bottle import post, request, route, run, static_file
from openai import OpenAI


class db:
    def create():
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS picture_openai(
            path,
            description
        );
        """
        )
        conn.commit()
        conn.close()

    def new(path, description):
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "insert into picture_openai(path, description) values(?,?)"
        cursor.execute(sql, (path, description))
        conn.commit()
        conn.close()

    def find(query):
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "select * from picture_openai where description like ?"
        result = cursor.execute((sql), (f"%{query}%",))
        result = result.fetchall()
        conn.close()

        return result


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

    with open(f"./pic_openai/{filename}", "wb") as handler:
        handler.write(img_data)

    return filename


def gallery(query):
    pictures = db.find(query)
    gallery = ""
    for image in pictures:
        gallery += f"""
                    <div style="display:inline-block; vertical-align:top; width:200px; height:auto;">
                        <img style="width:100%; height:auto;" src="./pic_openai/{image[0]}">
                        <p>{image[1]}<p>
                    </div>
                    """

    return gallery


@route("/", method=["GET", "POST"])
def index():
    query_create = request.forms.get("query_create")
    query_search = request.forms.get("query_search")

    current_image = ""
    if not query_search:
        query = ""
        image_gallery = gallery(query)

    if query_create:
        response = ai(query_create)
        image_url = response[0]
        revised_description = response[1]
        filename = download(image_url)
        db.new(filename, revised_description)
        current_image = f"""
            <img style='height:400px;width:auto;' src="./pic_openai/{filename}">
            <p>{revised_description}</p>
            <hr>
            """
    elif query_search:
        image_gallery = gallery(query_search)
    else:
        current_image = ""

    page = f"""
            <h1>Web App</h1>
            <form action="/" method="post">
                Create an Image: <input type="text" name="query_create">
                <br>
                Search for an Image: <input type="text" name="query_search">
                <br>
                <input type="submit">
            </form>
            <strong>{query_create}{query_search}</strong><br>
            {current_image}<br>
            {image_gallery}
            """
    return page


@route("/pic_openai/<filename:path>")
def serve_static(filename):
    return static_file(filename, root="./pic_openai")


db.create()
run(host="localhost", port=8080)
