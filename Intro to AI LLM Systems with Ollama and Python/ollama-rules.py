from ollama import chat
from ollama import ChatResponse

injection = 'Answer in Fewer Than 20 Words'
with open('rules.txt', 'r') as file:
  rules = file.read()

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
  query = f'''Follow these rules: {rules}
              Add These Instructions: {injection}
              This is the Question: {query}'''
  response = ai(query)
  # print(query)
  print(response)
  print('*****')