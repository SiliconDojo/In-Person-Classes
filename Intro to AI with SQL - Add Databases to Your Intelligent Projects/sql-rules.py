import sqlite3

from ollama import ChatResponse, chat


class db:
    def create():
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS rule (
            rule
        );
        """
        )

        conn.commit()
        conn.close()

    def rule_new(rule):
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "insert into rule(rule) values(?)"
        cursor.execute(sql, (rule,))
        conn.commit()
        conn.close()

    def rule_list():
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "select rowid,rule from rule"
        result = cursor.execute(sql)
        result = result.fetchall()
        conn.close()

        rules = ""
        for value in result:
            rules += f"{value[0]} - {value[1]}\n"

        return rules

    def rule_delete(rule):
        conn = sqlite3.connect("ai-class.db")
        cursor = conn.cursor()
        sql = "delete from rule where rowid = ?"
        cursor.execute(sql, (rule,))
        conn.commit()
        conn.close()


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
    query = input("How Can I Help: (please/list/delete) ")
    if "please" in query:
        db.rule_new(query)
        rules = db.rule_list()
        print(rules)
    elif "list" in query:
        rules = db.rule_list()
        print(rules)
    elif "delete" in query:
        rule = query.split(" ")
        rule[1] = rule[1].strip()
        db.rule_delete(rule[1])
        rules = db.rule_list()
        print(rules)

    else:
        rules = db.rule_list()
        query = f"""
              \nFollow these rule:
              \n{rules} 
              -- 
              \nTo Answer this query: 
              \n{query}
              """
        response = ai(query)
        # print(query)
        print(response)
        print("-----")
