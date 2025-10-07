from ollama import chat
from ollama import ChatResponse

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
  query = f'{injection} -- {query}'
  response = ai(query)
  print(response)
  print('*****')