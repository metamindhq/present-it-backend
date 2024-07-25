from pydantic import BaseModel


class ImageGenerationInput(BaseModel):
    image_generation_prompt: str


class ImageGenerationOutput(BaseModel):
    image_generation_prompt: str
    image_public_url: str
