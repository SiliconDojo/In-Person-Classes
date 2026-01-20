from openai import OpenAI


def ai(query):
    key = "YOUR API KEY"

    client = OpenAI(api_key=key)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": query},
                    {
                        "type": "input_image",
                        "image_url": "https://media.cnn.com/api/v1/images/stellar/prod/220905075014-02-nfl-glossary.jpg",
                    },
                ],
            }
        ],
    )

    return response.output_text


while True:
    query = input("Your Question: ")
    response = ai(query)
    print(query)
    print(response)
    print("****")
