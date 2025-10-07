from ollama import chat
from ollama import ChatResponse
from bs4 import BeautifulSoup
import requests

injection = 'Answer in Fewer Than 20 Words'

page = requests.get('https://arstechnica.com/ai/2025/10/openai-wants-to-make-chatgpt-into-a-universal-app-frontend/').text
#print(page)

soup = BeautifulSoup(page, "html.parser")
paragraphs = soup.find_all("p")
page_text = ''
for line in paragraphs:
  page_text += line.text
#print(page_text)

def ai(query):
  response: ChatResponse = chat(model='gpt-oss', messages=[
    {
      'role': 'user',
      'content': query,
    },
  ])

  return response.message.content

while True:
  query = input('How Can I Help You: ')
  query = f'''
            Follow these rules: {injection}
            Answer This Query: {query}
            About this webpage: {paragraphs}
            '''
  response = ai(query)
  print(response)
  print('*****')
















