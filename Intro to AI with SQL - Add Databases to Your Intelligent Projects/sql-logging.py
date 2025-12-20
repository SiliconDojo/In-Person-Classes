import sqlite3

from ollama import ChatResponse, chat

injection = "Answer in under 10 words"


class db:
    def create():
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS thread (
            query,
            response,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        )

        conn.commit()
        conn.close()

    def insert(query, response):
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "insert into thread(query,response) values(?,?)"
        cursor.execute(sql, (query, response))
        conn.commit()
        conn.close()


def ai(query):
    response: ChatResponse = chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": query,
            },
        ],
    )

    return response.message.content


db.create()

while True:
    query = input("How Can I Help: ")
    query = f"{injection} -- {query}"
    response = ai(query)
    db.insert(query, response)
    print(query)
    print(response)
    print("-----")
