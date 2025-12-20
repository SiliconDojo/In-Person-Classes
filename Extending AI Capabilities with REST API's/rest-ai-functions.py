import func
from ollama import ChatResponse, chat

with open("func.py", "r") as file:
    functions = file.read()


def ai_llm(query, functions):
    response: ChatResponse = chat(
        model="gpt-oss",
        messages=[
            {
                "role": "user",
                "content": f"""
        1. Query: {query}
        2. Which Function from this list of Functions is best for the query. 
        3. Answer only with the function, and no other words.
        4. Functions: {functions}
        """,
            },
        ],
    )
    return response.message.content


def ai_response(query, data):
    response: ChatResponse = chat(
        model="gpt-oss",
        messages=[
            {
                "role": "user",
                "content": f"""
      1. Answer this query and nothing else
      2. Make the answer short
      3. Query: {query}
      4. Based off of this information: {data}

        """,
            },
        ],
    )
    return response.message.content


while True:
    query = input("Question: ")
    response = ai_llm(query, functions)
    print(response)
    response = response.replace("()", "")

    if hasattr(func, response):
        fn = getattr(func, response)
        response = fn()
    else:
        print("No such function in func.py:", response)

    print(response)
    ai_answer = ai_response(query, response)
    print(ai_answer)
