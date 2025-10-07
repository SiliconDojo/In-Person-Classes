from ollama import chat
from ollama import ChatResponse

injection = 'Reply in Fewer Than 20 Words. Only Answer current query:'

with open('memory.txt', 'w') as file:
  file.write('This is the conversation we have had up until now.\n\n')

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
  memory = open('memory.txt').read()
  query_full = f'Injection: {injection} \n\n Query: {query} \n\n  Memory: {memory}'
  response = ai(query_full)
  with open('memory.txt', 'a') as file:
    file.write(f'Me: {query}\n')
    file.write(f'You: {response}\n')
  print(response)
  print('*****')