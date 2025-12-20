import os
from pathlib import Path

from openai import OpenAI

key = "YOUR API KEY"

client = OpenAI(api_key=key)

speech_file_path = Path(__file__).parent / "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",  # verse, echo, fable, onyx
    input="Louis Rossmann is a stinky face",
    instructions="Speak in a cheerful and positive tone.",
) as response:
    response.stream_to_file(speech_file_path)

os.system("afplay speech.mp3")
