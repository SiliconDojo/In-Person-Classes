from ollama import chat
from ollama import ChatResponse
from bottle import run, route, post, request
from bs4 import BeautifulSoup
import requests

def ai_post(blog_text):
  response: ChatResponse = chat(model='gpt-oss', messages=[
    {
      'role': 'user',
      'content': f'Rewrite this in under 500 words --- {blog_text}.',
    },
  ])
  return response.message.content

def ai_title(post):
  response: ChatResponse = chat(model='gpt-oss', messages=[
    {
      'role': 'user',
      'content': f'Provide a title for this blog post in uder 10 words --- {post}',
    },
  ])
  return response.message.content
   
def scrape(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    paragraphs = soup.find_all("p")
    page_text = ''
    for line in paragraphs:
        page_text += line.text

    return page_text

@route('/', method=['GET','POST'])
def index():
    url = request.forms.get('url')
    if url:
        blog_text = scrape(url)
        post = ai_post(blog_text)
        title = ai_title(post)
        with open('blog.html', 'a') as file:
            file.write(f'<h1>{title}</h1>')
            file.write(f'{post}<hr>')
    else:
        url = ''
        title = ''
        post = ''
        blog_text = ''

    page = f'''
            <h1>Web App</h1>
            <form action="/" method="post">
                URL: <input type="text" name="url">
                <input type="submit">
            </form>
            <h3>URL:</h3> {url}<br>
            <h3>Title:</h3> {title}<br>
            <h3>New Post:</h3> {post}<br>
            <h3>Original Text:</h3> {blog_text}
            '''
    return page

run(host='localhost', port=8080)
