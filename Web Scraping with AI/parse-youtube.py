from youtube_transcript_api import YouTubeTranscriptApi

video_id = "-w6fIHXas4o"

ytt_api = YouTubeTranscriptApi()
fetched_transcript = ytt_api.fetch(video_id)

for snippet in fetched_transcript:
    print(snippet)
    # print(snippet.text)
    # print(f'{snippet.start} -- {snippet.text}')
