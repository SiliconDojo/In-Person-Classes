from openai import OpenAI

key = "YOUR API KEY"

client = OpenAI(api_key=key)

response = client.responses.create(
    model="gpt-5", input="Write a one-sentence joke about Louis Rossmann"
)
print(response)
print("****")
print(response.output_text)
print("****")
print(response.usage.total_tokens)
