from pydantic import BaseModel


class PresentationAudioInput(BaseModel):
    audio_generation_prompt: str = "Sample audio generation prompt"
    audio_voice: str = "Scarlett"
    speed: float = 0.25
    pitch: float = 1


class PresentationAudioOutput(PresentationAudioInput):
    audio_public_url: str
    audio_length_in_sec: int
