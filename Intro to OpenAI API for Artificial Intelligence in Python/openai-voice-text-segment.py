from openai import OpenAI

key = "YOUR API KEY"

client = OpenAI(api_key=key)

audio_file = open("openai-test-audio.m4a", "rb")

transcript = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-1",
    response_format="verbose_json",
    timestamp_granularities=["segment"],
)
print(transcript)
print("****")

for segment in transcript.segments:
    start = segment.start
    end = segment.end
    text = segment.text
    print(f"{start:.2f}s - {end:.2f}s: {text}")
