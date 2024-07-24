import dspy
import os
import logging
from presentation import PresentationManager
from presentation import PresentationInput, PresentationOutput
from util.imageloader import ImageLoader
from fastapi import FastAPI

# In case of development, load the .env file
if not os.getenv("ENV") == "production":
    from dotenv import load_dotenv
    load_dotenv()

lm = dspy.OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAPI_API_KEY"))
dspy.settings.configure(lm=lm)
image_loader = ImageLoader(
    bucket=os.getenv("AWS_S3_BUCKET_NAME"),
    access_key=os.getenv("AWS_ACCESS_KEY"),
    secret_key=os.getenv("AWS_SECRET_KEY")
)
# This is the main entry point for the application


app = FastAPI()
LOGGER = logging.getLogger(__name__)


@app.post("/generate")
def generate_slides(presentation_input: PresentationInput) -> PresentationOutput:
    presentation_manager = PresentationManager(presentation_input, image_loader)
    slide = presentation_manager.generate_next_slide()
    return slide
