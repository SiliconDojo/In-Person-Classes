import sqlite3

from ollama import ChatResponse, chat

injection = "Answer in 10 words or fewer. Only answer the question"


class db:
    def create():
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS memory (
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
        sql = "insert into memory(query, response) values(?,?)"
        cursor.execute(sql, (query, response))
        conn.commit()
        conn.close()

    def remember():
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "select * from memory limit 10"
        result = cursor.execute(sql)
        result = result.fetchall()
        conn.close()

        memory = ""
        for value in result:
            memory += f"Query: {value[0]}\n Response: {value[1]}\n"

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
    memory = db.remember()
    print(memory)
    query_full = f"""
                Answer this query: {query}\n
                Follow these rule: {injection}\n
                This is our conversation until now: {memory}\n
                """
    response = ai(query_full)
    db.new(query, response)

    print(query)
    print(response)
    print("-----")
