from bottle import post, request, route, run
from ollama import ChatResponse, chat
from youtube_transcript_api import YouTubeTranscriptApi


def ai(transcript, query):
    response: ChatResponse = chat(
        model="gpt-oss",
        messages=[
            {
                "role": "user",
                "content": f"""
            Answer this question: {query}
            About this transcript of a Youtube Video: {transcript}.
            """,
            },
        ],
    )
    return response.message.content


def scrape(url):
    url = url.split("=")
    video_id = url[1]

    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)

    transcript_clean = ""
    for snippet in transcript:
        transcript_clean += f"Start Time: {snippet.start} Text: {snippet.text}<br>"

    return transcript_clean


def embed(url):
    url = url.split("=")
    video_id = url[1]
    embed = f"""
        <iframe width="560" height="315"
            src="https://www.youtube.com/embed/{video_id}"
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
        <br>
    """
    return embed


@route("/", method=["GET", "POST"])
def index():
    query = request.forms.get("query")
    if not query:
        query = ""

    url = request.forms.get("url")
    if not url:
        url = ""
        transcript = ""
    else:
        transcript = scrape(url)

    if url != "" and transcript != "":
        response = ai(transcript, query)
        youtube_embed = embed(url)
    else:
        response = "*****"
        youtube_embed = "*****"

    page = f"""
            <h1>Web App</h1>
            <form action="/" method="post">
                Video: <input type="text" name="url" value="{url}">
                Search: <input type="text" name="query">
                <br>
                <input type="submit">
            </form>
            {youtube_embed}
            <strong>{query}</strong><br>
            <p>{response}</p>
            {transcript}
            """
    return page


run(host="localhost", port=8080)
