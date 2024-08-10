from pydantic import BaseModel, Field


class PresentationInputBase(BaseModel):
    topic: str
    color_scheme: str
    target_audience: str
    total_slides: int = 5
    current_slide_number: int = 0


class PresentationInput(PresentationInputBase):
    previous_slides_summaries: str = ""


class PresentationOutput(BaseModel):
    title: str
    subtitle: str
    content: str
    bullet_points: list[str]
    speaker_note: str
    summary: str
    image_generation_prompt: str 


class PresentationTitleSubtitleInput(BaseModel):
    topic: str = Field(description="Topic or idea of the presentation")
    target_audience: str = Field(description="Intended audience for the presentation")
    current_slide_number: str = Field(description="Current slide number")
    total_slides: str = Field(description="Total number of slides in the presentation")
    previous_slide_summaries: str = Field(description="Summary of the previous slides for context",
                                          default=None)


class PresentationTitleSubtitleOutput(BaseModel):
    title: str = Field(description="Think of a unique, catchy title for the slide with the main idea !!WARNING don't "
                                   "format the texts")
    subtitle: str = Field(description="Think of a subtitle that complements the title and provides more context "
                                      "!!WARNING don't format the texts")


class PresentationContentInput(PresentationTitleSubtitleInput):
    title: str = Field(description="Title of the slide, less than 5 words")
    subtitle: str = Field(description="Subtitle of the slide in less than 10 words")
    current_slide_number: str = Field(description="Current slide number")
    total_slides: str = Field(description="Total number of slides in the presentation")


class PresentationContentOutput(BaseModel):
    content: str = Field(description="Generated content for the slide in less than 50 words, to be used before "
                                     "presenting bullet points,"
                                     "!!WARNING don't format the texts and don't mention word like this slide, "
                                     "in this presentation")


class PresentationBulletPointsInput(BaseModel):
    title: str = Field(description="Title of the slide")
    subtitle: str = Field(description="Subtitle of the slide")
    topic: str = Field(description="Topic or idea of the presentation")
    target_audience: str = Field(description="Intended audience for the presentation")
    content: str = Field(description="Content of the slide")
    previous_bullet_points: str = Field(description="Previous bullet points for context if exists, separated by commas",
                                        default=None)


class PresentationBulletPointsOutput(BaseModel):
    next_bullet_point: str = Field(description="Next bullet point for the slide")


class PresentationSpeakerNoteInput(PresentationContentInput):
    content: str = Field(description="Content of the slide")
    bullet_points: str = Field(description="Bullet points for the slide")
    summaries: str = Field(description="Summaries of the previous slides for context")
    current_slide_number: str = Field(description="Current slide number")
    total_slides: str = Field(description="Total number of slides in the presentation")


class PresentationSpeakerNoteOutput(BaseModel):
    speaker_note: str = Field(description="Speaker notes for the slide, this is the content user will read out "
                                          "loud to the audience, be simple and clear !!WARNING don't format "
                                          "the texts")
    summary: str = Field(description="Summary of the slide content in detail on what it is about")


class PresentationImageGenerationPromptInput(BaseModel):
    topic: str = Field(description="Topic or idea of the presentation")
    target_audience: str = Field(description="Intended audience for the presentation")
    summary: str = Field(description="Summary of the slide content for context and coherence with previous slides")
    color_scheme: str = Field(description="Color scheme of the presentation")


class PresentationImageGenerationPromptOutput(BaseModel):
    image_generation_prompt: str = Field(description="Prompt for image generation aligned with the slide's content, "
                                                     "to be used to generate images for the slide using generation "
                                                     "models"
                                                     "add better image contexts here, like the type of image, the color"
                                                     "scheme, the style, the mood, etc and strictly no text in the "
                                                     "image")
