from ollama import chat
from ollama import ChatResponse

injection = 'Answer in Fewer Than 20 Words'
filter = ['hipster', 'monster', 'red hat', 'blue hair']

def bad_question(query):
    response: ChatResponse = chat(model='phi3', messages=[
        {
        'role': 'user',
        'content': f'''Reply with only "YES" or "NO".
                        Is this query about computers?
                        QUERY: {query},
                        '''
        },
    ])

    return response.message.content

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

    check = bad_question(query)
    
    if any(word in query for word in filter):
        print("You can't say that")
    elif 'no' in check.lower():
        print("Keep your query on topic")
    else:
        query = f'{injection} -- {query}'
        response = ai(query)
        print(response)
        print('*****')
  
   