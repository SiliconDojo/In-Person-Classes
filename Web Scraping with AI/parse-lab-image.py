import os
import sqlite3
import time

import requests
from bs4 import BeautifulSoup
from ollama import ChatResponse, chat


class db:
    def create():
        conn = sqlite3.connect("image.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS image (
            pic,
            filename,
            description
        );
        """
        )
        conn.commit()
        conn.close()

    def new(pic, filename, description):
        conn = sqlite3.connect("image.db")
        cursor = conn.cursor()
        sql = "insert into image(pic, filename, description) values(?,?,?)"
        cursor.execute(sql, (pic, filename, description))
        conn.commit()
        conn.close()

    def find(pic):
        conn = sqlite3.connect("image.db")
        cursor = conn.cursor()
        sql = "select * from image where pic = ?"
        result = cursor.execute(sql, (pic,))
        result = result.fetchone()
        conn.close()

        return result


def ai(filename):
    response: ChatResponse = chat(
        model="llava",
        messages=[
            {
                "role": "user",
                "content": """
                        Provide 10 tags for this image.
                        These tags will be used for search on a web app.
                        Return in CSV format
                    """,
                "images": [filename],
            }
        ],
    )
    response = response.message.content
    return response


def scrape(url):
    image_list = []
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    images = soup.find_all("img")
    for image in images:
        pic = image.get("src")
        image_list.append(pic)
    return image_list


def download(url):
    ext = os.path.splitext(url)[1]
    filename = f"{time.time()}{ext}"
    response = requests.get(url).content
    with open(f"./pics/{filename}", "wb") as file:
        file.write(response)
    return filename


db.create()

while True:
    try:
        url = input("URL: ")
        pics = scrape(url)
        for pic in pics:
            print(pic)
            if not db.find(pic):
                filename = download(pic)
                print(filename)
                description = ai(f"./pics/{filename}")
                print(description)
                db.new(pic, filename, description)
    except:
        print("Page could not be processed")
