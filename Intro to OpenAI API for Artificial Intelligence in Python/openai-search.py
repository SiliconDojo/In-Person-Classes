from openai import OpenAI

key = "YOUR API KEY"

client = OpenAI(api_key=key)

response = client.responses.create(
    model="gpt-5", tools=[{"type": "web_search"}], input="What happened with tariffs today"
)

print(response.output_text)
