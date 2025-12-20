import sqlite3

from ollama import ChatResponse, chat


class db:
    def create():
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS cache (
            query,
            response
        );
        """
        )
        conn.commit()
        conn.close()

    def new(query, response):
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "insert into cache(query, response) values(?,?)"
        cursor.execute(sql, (query, response))
        conn.commit()
        conn.close()

    def find(query):
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "select query,response from cache where query like ?"
        result = cursor.execute(sql, (query,))
        result = result.fetchone()
        conn.close()

        return result


def ai(query):
    response: ChatResponse = chat(
        model="gpt-oss",
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
    query = input("How Can I Help:")
    find = db.find(query)
    print(find)
    if find:
        print(find[0])
        print(find[1])
    else:
        response = ai(query)
        db.new(query, response)
        print(query)
        print(response)
        print("-----")
