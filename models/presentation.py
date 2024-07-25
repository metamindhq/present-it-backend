from pydantic import BaseModel


class PresentationInputBase(BaseModel):
    topic: str
    color_scheme: str
    target_audience: str
    total_slides: int = 5
    current_slide_number: int = 0


class PresentationInput(PresentationInputBase):
    previous_slides_summaries: list[str] = []


class PresentationOutput(BaseModel):
    title: str
    subtitle: str
    content: str
    bullet_points: list[str]
    speaker_note: str
    summary: str
    image_generation_prompt: str
