from ollama import chat
from ollama import ChatResponse
import requests

location = requests.get('http://ip-api.com/json/').json()
location = location['country']

injection = 'Answer in Fewer Than 20 Words'

def ai(query):
  response: ChatResponse = chat(model='phi3', messages=[
    {
      'role': 'user',
      'content': query,
    },
  ])

  return response.message.content

while True:
  query = input('How Can I Help You: ')
  query = f'''Add These Instructions: {injection}
              I am from: {location}
              This is the Question: {query}'''
  response = ai(query)
# print(query)
  print(location)
  print(response)
  print('*****')