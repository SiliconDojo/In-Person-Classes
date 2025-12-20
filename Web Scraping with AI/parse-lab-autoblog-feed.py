import sqlite3

import feedparser
import requests
from bs4 import BeautifulSoup
from ollama import ChatResponse, chat

sites = [
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://techcrunch.com/feed/",
    "https://gizmodo.com/feed",
]

instructions = """
                Write a 500 Word Blog Post.
                Always be excited and upbeat.
                Say "Dude" in post.
                """


class db:
    def create():
        conn = sqlite3.connect("autoblog.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS blog (
            title,
            url,
            post_original,
            title_ai,
            post_ai
        );
        """
        )
        conn.commit()
        conn.close()

    def new(title, url):
        conn = sqlite3.connect("autoblog.db")
        cursor = conn.cursor()
        sql = "insert into blog(title, url) values(?,?)"
        cursor.execute(sql, (title, url))
        conn.commit()
        conn.close()

    def find(title):
        conn = sqlite3.connect("autoblog.db")
        cursor = conn.cursor()
        sql = "select * from blog where title like ?"
        result = cursor.execute(sql, (title,))
        result = result.fetchone()
        conn.close()

        return result

    def index():
        conn = sqlite3.connect("autoblog.db")
        cursor = conn.cursor()
        sql = "select * from blog where post_ai IS NULL"
        result = cursor.execute(sql)
        result = result.fetchall()
        conn.close()

        return result

    def update_original(url, text, text_ai, title_ai):
        conn = sqlite3.connect("autoblog.db")
        cursor = conn.cursor()
        sql = """
            update blog set post_original = ?,
            post_ai = ?,
            title_ai = ?
            where url = ?
            """
        cursor.execute(sql, (text, text_ai, title_ai, url))
        conn.commit()
        conn.close()


def ai_post(page, instructions):
    response: ChatResponse = chat(
        model="gpt-oss",
        messages=[
            {
                "role": "user",
                "content": f"""
                Follow these Instructions: {instructions}
                Use this information to create the post: {page}.
                """,
            },
        ],
    )
    return response.message.content


def ai_title(post):
    response: ChatResponse = chat(
        model="gpt-oss",
        messages=[
            {
                "role": "user",
                "content": f"""
                Create a Title for this blog post that is 10 words or less. 
                Return only the title and no other instructions.
                Do not mention "Title"
                {post}
                """,
            },
        ],
    )
    return response.message.content

    response: ChatResponse = chat(
        model="gpt-oss",
        messages=[
            {
                "role": "user",
                "content": f"""
                Provide 10 tags for this blog post. Return in CSV format. {post}
                """,
            },
        ],
    )
    return response.message.content


def scrape_post(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    paragraphs = soup.find_all("p")

    page_clean = ""
    for line in paragraphs:
        page_clean += line.get_text()

    return page_clean


def scrape_feed(site):
    d = feedparser.parse(site)
    for value in d.entries:
        title = value.title
        link = value.links[0].href
        if not db.find(title):
            db.new(title, link)


db.create()

for site in sites:
    scrape_feed(site)

que = db.index()

# print(que)

for post in que:
    try:
        url = post[1]
        text = scrape_post(url)
        print(f"Text Scraped: {url}")
        text_ai = ai_post(text, instructions)
        print(f"Text AI Processed: {url}")
        title_ai = ai_title(text_ai)
        print(f"Title Created: {url}")
        db.update_original(url, text, text_ai, title_ai)
    except:
        pass
