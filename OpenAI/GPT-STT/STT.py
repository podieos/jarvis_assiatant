from openai import OpenAI

client = OpenAI(api_key="API_KEY")

FILE = "audio.mp3"

with open(FILE, "rb") as f:
    result = client.audio.transcriptions.create(
        model="whisper-1",
        file=(FILE, f, "audio/mpeg")
    )
    print(result.text)