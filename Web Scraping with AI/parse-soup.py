import requests
import tiktoken
from bs4 import BeautifulSoup

page = requests.get(
    "https://arstechnica.com/space/2025/11/nasa-is-kind-of-a-mess-here-are-the-top-priorities-for-a-new-administrator/"
).text

soup = BeautifulSoup(page, "html.parser")
paragraphs = soup.find_all("p")

page_clean = ""
for line in paragraphs:
    page_clean += line.get_text()

print(page_clean)

encoding = tiktoken.encoding_for_model("gpt-4")
tokens = encoding.encode(page_clean)

print(f"Number of tokens: {len(tokens)}")
