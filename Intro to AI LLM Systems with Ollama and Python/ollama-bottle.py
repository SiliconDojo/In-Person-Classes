from ollama import chat
from ollama import ChatResponse
from bottle import run, route, post, request

injection = 'Answer in Fewer Than 20 Words.'

def ai(query):
  response: ChatResponse = chat(model='phi3', messages=[
    {
      'role': 'user',
      'content': query,
    },
  ])
  return response.message.content

@route('/', method=['GET','POST'])
def index():
    query = request.forms.get('query')

    query_full = f'{injection} -- {query}'
    response = ai(query_full)

    page = f'''
            <h1>Web App</h1>
            <form action="/" method="post">
                How Can I help: <input type="text" name="query">
                <br>
                <input type="submit">
            </form>
            <strong>{query}</strong><br>
            {response}
            '''
    return page

run(host='localhost', port=8080)