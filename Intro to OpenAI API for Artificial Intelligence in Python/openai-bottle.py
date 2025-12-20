from bottle import post, request, route, run
from openai import OpenAI

injection = "Answer in Fewer Than 20 Words."


def ai(query):
    key = "YOUR API KEY"

    client = OpenAI(api_key=key)

    response = client.responses.create(model="gpt-5-nano", input=query)
    return response.output_text


@route("/", method=["GET", "POST"])
def index():
    query = request.forms.get("query")

    if query:
        query_full = f"{injection} -- {query}"
        response = ai(query_full)
    else:
        response = "***"

    page = f"""
            <h1>Web App</h1>
            <form action="/" method="post">
                How Can I help: <input type="text" name="query">
                <br>
                <input type="submit">
            </form>
            <strong>{query}</strong><br>
            {response}
            """
    return page


run(host="localhost", port=8080)
