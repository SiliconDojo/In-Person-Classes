from openai import OpenAI

key = "YOUR API KEY"

client = OpenAI(api_key=key)

response = client.responses.create(
    model="gpt-5", input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
