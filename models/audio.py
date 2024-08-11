from pydantic import BaseModel
class PresentationAudioInput(BaseModel):
    audio_generation_prompt: str = "Sample audio generation prompt"
    audio_voice: str = "Scarlett"


class PresentationAudioOutput(PresentationAudioInput):
    audio_public_url: str