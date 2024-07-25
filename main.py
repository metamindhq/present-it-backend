from typing import Dict, Any

import dspy
import os
import logging
from presentation import PresentationManager
from presentation import PresentationInput, PresentationOutput
from models.image import ImageGenerationInput, ImageGenerationOutput
from util.imageloader import ImageLoader
from util.gcp import get_gcp_storage_client
from fastapi import FastAPI

# In case of development, load the .env file
if not os.getenv("ENV") == "production":
    from dotenv import load_dotenv

    load_dotenv()

lm = dspy.OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAPI_API_KEY"))
dspy.settings.configure(lm=lm)
image_loader = ImageLoader(
    bucket_name=os.getenv("GCP_OBJECT_STORE_BUCKET"),
    storage_client=get_gcp_storage_client(os.getenv("GCP_PROJECT_ID"))
)

app = FastAPI()
LOGGER = logging.getLogger(__name__)

presentation_manager = PresentationManager(image_loader)


@app.post("/generate")
def generate_slides(presentation_input: PresentationInput) -> PresentationOutput:
    slide = presentation_manager.generate_next_slide(presentation_input)
    return slide


@app.post("/generate/image")
def generate_slides(image_generation_prompt: ImageGenerationInput) -> ImageGenerationOutput:
    return presentation_manager.generate_image_by_prompt(image_generation_prompt)
