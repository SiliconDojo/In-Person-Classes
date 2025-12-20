import feedparser
from openai import OpenAI

feeds = [
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://techcrunch.com/feed/",
    "https://gizmodo.com/feed",
]

posts = []


def process(feed, posts):
    d = feedparser.parse(feed)

    for value in d.entries:
        posts.append({"site": feed, "title": value.title})


def ai(query, posts):
    key = "YOUR API KEY"

    client = OpenAI(api_key=key)

    response = client.responses.create(
        model="gpt-5",
        input=f"""
                Answer in fewer than 50 words
                Answer this question: {query}
                About this News Feed: {posts}
                """,
    )

    response = response.output_text
    return response


for site in feeds:
    process(site, posts)

while True:
    query = input("Question?:   ")
    response = ai(query, posts)
    print(response)
