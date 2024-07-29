import dspy
import os
import logging
from presentation import PresentationManager
from presentation import PresentationInput, PresentationOutput
from models.image import ImageGenerationInput, ImageGenerationOutput
from util.imageloader import ImageLoader
from util.gcp import get_gcp_storage_client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import weave

# In case of development, load the .env file
if not os.getenv("ENV") == "production":
    from dotenv import load_dotenv

    load_dotenv()

system_prompt = """You are an advanced AI system designed to generate high-quality, professional presentations. For 
each slide, . Maintain a professional, authoritative tone throughout the presentation, ensuring coherence and logical flow between slides. Adapt content complexity to the specified audience 
and purpose, incorporating the given color scheme consistently across all elements. Use concise, impactful language 
to maximize engagement. Focus each slide on a single main idea, use the "rule of three" when applicable, 
and incorporate relevant data or examples to support key points. Create smooth transitions between major sections, 
and end with a strong closing slide. Maintain consistency in terminology, phrasing, and level of detail across all 
slides, while adjusting language complexity based on the target audience. For visual elements, suggest appropriate 
chart types, recommend complementary icons or symbols, and provide guidance on image composition and style in the 
image generation prompts, ensuring all visual elements align with the specified color scheme."""

lm = dspy.OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAPI_API_KEY"), system_prompt=system_prompt,
                 temperature=0.7)
dspy.settings.configure(lm=lm)
dspy.settings.experimental = True
image_loader = ImageLoader(
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


@app.post("/generate")
def generate_slides(presentation_input: PresentationInput) -> PresentationOutput:
    slide = presentation_manager.generate_next_slide(presentation_input)
    return slide


@app.post("/generate/image")
def generate_slides(image_generation_prompt: ImageGenerationInput) -> ImageGenerationOutput:
    return presentation_manager.generate_image_by_prompt(image_generation_prompt)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
