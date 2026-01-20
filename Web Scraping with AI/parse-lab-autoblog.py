import requests
from bs4 import BeautifulSoup
from ollama import ChatResponse, chat


def ai(query, page):
    response: ChatResponse = chat(
        model="gpt-oss",
        messages=[
            {
                "role": "user",
                "content": f"""
        Write a blog post in under 500 words.
        Follow these instruction: {query}
        Use this information to create the post: {page}.
        """,
            },
        ],
    )
    return response.message.content


def scrape(site):
    page = requests.get(site).text
    soup = BeautifulSoup(page, "html.parser")
    paragraphs = soup.find_all("p")

    page_clean = ""
    for line in paragraphs:
        page_clean += line.get_text()

    return page_clean


while True:
    site = input("URL: ")
    query = input("Instructions: ")
    page = scrape(site)
    response = ai(query, page)
    print(response)

    with open("blog.html", "w") as file:
        response = response.split("\n")
        file.write('<meta charset="UTF-8">')
        for line in response:
            file.write(f"<p>{line}</p>")
            print(line)
