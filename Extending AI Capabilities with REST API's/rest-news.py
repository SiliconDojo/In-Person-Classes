import requests
from ollama import ChatResponse, chat


def get_news():
    key = "YOUR API KEY"
    response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}").json()

    news = ""
    for article in response["articles"]:
        news += (
            f"{article['source']['name']}\n"
            f"{article['title']}\n"
            f"{article['description']}\n"
            "****\n"
        )
    print(news)

    return news


def ai(query, news):
    response: ChatResponse = chat(
        model="gpt-oss",
        messages=[
            {
                "role": "user",
                "content": f"""
        1. Answer as short as possible.
        2. Do not add additional information beyond the answer.
        3. Answer this query: {query}
        4. Based on this News: {news}.
        """,
            },
        ],
    )
    return response.message.content


news = get_news()
while True:
    query = input("Question: ")
    response = ai(query, news)
    print(response)
