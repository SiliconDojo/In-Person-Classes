import requests
import tiktoken

page = requests.get(
    "https://arstechnica.com/space/2025/11/nasa-is-kind-of-a-mess-here-are-the-top-priorities-for-a-new-administrator/"
).text

print(page)

encoding = tiktoken.encoding_for_model("gpt-4")
tokens = encoding.encode(page)

print(f"Number of tokens: {len(tokens)}")
