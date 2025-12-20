from ollama import ChatResponse, chat


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


while True:
    query = input("How Can I Help: ")
    response = ai(query)
    print(query)
    print(response)
    print("-----")
