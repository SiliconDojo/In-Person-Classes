import os
import sqlite3

from ollama import ChatResponse, chat


class db:
    def create():
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS picture (
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
        sql = "insert into picture(path, description) values(?,?)"
        cursor.execute(sql, (path, description))
        conn.commit()
        conn.close()

    def find(query):
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "select * from picture where description like ?"
        result = cursor.execute(sql), (f"%{query}%")
        result = result.fetchall()
        conn.close()

        return result


def ai(query):
    response = chat(
        model="llava",
        messages=[
            {
                "role": "user",
                "content": """
                            Describe this image.
                            Specify each food product.
                            Include any brand names.
                            Include the nationality of the food.
                            """,
                "images": [f"./pic/{query}"],
            }
        ],
    )

    return response["message"]["content"]


db.create()

pictures = os.listdir("./pic")
for name in pictures:
    response = ai(name)
    db.new(name, response)
    print(f"{name} -- Processed")
