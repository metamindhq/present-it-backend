import dspy
import os
import logging

from openai import OpenAI
from presentation import PresentationManager, generate_next_slide_using_openai
from presentation import PresentationInput, PresentationOutput
from models.image import ImageGenerationInput, ImageGenerationOutput
from models.audio import PresentationAudioInput, PresentationAudioOutput
from util.fileloader import FileLoader
from util.gcp import get_gcp_storage_client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import weave

# In case of development, load the .env file
if not os.getenv("ENV") == "development":
    from dotenv import load_dotenv

    load_dotenv()

system_prompt = """You are an advanced AI system designed to generate high-quality, professional presentations. For 
each slide, prioritize simplicity, clarity, and engagement in simple and technical language. Create a clear, 
concise title that reflects the main point. Limit content to 3-5 key points using brief, impactful phrases. 
Incorporate relevant data, statistics, or examples, and suggest appropriate visuals. Provide detailed speaker notes 
with context, potential audience questions, and transition phrases. Include a 2-3 sentence summary of key takeaways 
to inform the next slide's content. If previous slides summaries are provided, ensure coherence and logical flow. and 
try to put a different content for next slide"""

lm = dspy.OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAPI_API_KEY"), system_prompt=system_prompt,
                 temperature=0.7)
dspy.settings.configure(lm=lm)
dspy.settings.experimental = True
image_loader = FileLoader(
    bucket_name=os.getenv("GCP_OBJECT_STORE_BUCKET"),
    storage_client=get_gcp_storage_client(os.getenv("GCP_PROJECT_ID"))
)

app = FastAPI()

# Enable CORS
origins = ["*"]
methods = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)

LOGGER = logging.getLogger(__name__)
weave.init(project_name="dspy-canva-hackathon")

presentation_manager = PresentationManager(image_loader)

client = OpenAI(api_key=os.getenv("OPENAPI_API_KEY"))


@app.post("/openai/generate")
def generate_slides(presentation_input: PresentationInput):
    return generate_next_slide_using_openai(presentation_input, client)


@app.post("/generate/image")
def generate_slides(image_generation_prompt: ImageGenerationInput) -> ImageGenerationOutput:
    return presentation_manager.generate_image_by_prompt(image_generation_prompt)


@app.post("/generate/audio")
def generate_audio(audio_generation_prompt: PresentationAudioInput) -> PresentationAudioOutput:
    return presentation_manager.generate_audio_by_prompt(audio_generation_prompt)


@app.post("/generate", deprecated=True)
def generate_slides(presentation_input: PresentationInput) -> PresentationOutput:
    slide = presentation_manager.generate_next_slide(presentation_input)
    return slide


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
