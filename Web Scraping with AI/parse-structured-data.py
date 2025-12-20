import json

from ollama import chat

with open("message.txt", "r") as file:
    text = file.read()

response = chat(
    model="gpt-oss",
    messages=[
        {
            "role": "user",
            "content": f"""
             Provide all of the names and email addresses from this document in usable JSON format
            Like {{'contacts':[{{'name':'bob', 'email:'bob@aol.com'}},{{'name':'sue','email':'sue@aol.com'}}]}}
            Text: {text}
            """,
        }
    ],
    format="json",
)
response = response.message.content
response = json.loads(response)
print(response)

for x in response["contacts"]:
    print(f"{x['name']} -- {x['email']}")
