from openai import OpenAI

key = "YOUR API KEY"

client = OpenAI(api_key=key)

audio_file = open("openai-test-audio.m4a", "rb")
transcript = client.audio.transcriptions.create(model="gpt-4o-transcribe", file=audio_file)

print(transcript)
print("****")
print(transcript.text)
