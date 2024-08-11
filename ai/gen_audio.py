import requests
import os

url = "https://api.v7.unrealspeech.com/stream"


def generate_audio(prompt: str, voice: str):
    available_voices = ["Scarlett", "Dan", "Liv", "Will", "Amy"]
    if voice not in available_voices:
        raise ValueError(f"Voice {voice} is not available. Available voices are {available_voices}")
    payload = {
        "Text": prompt,
        "VoiceId": voice,
        "Bitrate": "192k",
        "Speed": "0",
        "Pitch": "1",
        "Codec": "libmp3lame",
        "Temperature": 0.25
    }

    headers = {
        "accept": "text/plain",
        "content-type": "application/json",
        "Authorization": f"Bearer {os.getenv('UNREAL_SPEECH_API_KEY')}"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.content
