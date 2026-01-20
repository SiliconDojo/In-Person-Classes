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

    def select():
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "select * from thread"
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return result


def report():
    response = db.select()
    with open("ai-report-clean.html", "w") as file:

        file.write("<table>")
        for line in response:
            request = line[0].replace(f"{injection} -- ", "")
            file.write(
                f"""
                   <tr>
                      <td>{request}</td>
                      <td>{line[1]}</td>
                      <td>{line[2]}</td>
                   </tr>
                   """
            )
        file.write("</table>")


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
    report()
    print(query)
    print(response)
    print("-----")
