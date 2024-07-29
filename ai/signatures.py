import dspy
from models.presentation import (PresentationTitleSubtitleInput, PresentationContentInput,
                                 PresentationBulletPointsInput,
                                 PresentationSpeakerNoteInput, PresentationImageGenerationPromptInput)


class TitleSubtitleGeneratorSignature(dspy.Signature):
    """
    Generate a title and subtitle for a presentation slide based on the main topic and context.
    """
    input: PresentationTitleSubtitleInput = dspy.InputField()
    title: str = dspy.OutputField(desc="Think of a unique, catchy title for the slide with the main idea !!WARNING "
                                       "don't"
                                       "format the texts")
    subtitle: str = dspy.OutputField(desc="Think of a subtitle that complements the title and provides more context "
                                          "!!WARNING don't format the texts")


class ContentGeneratorSignature(dspy.Signature):
    """
    Generate content for a presentation slide based on the main topic and context.
    """
    input: PresentationContentInput = dspy.InputField()
    content: str = dspy.OutputField(desc="Generated content for the slide, to be used before presenting bullet points, "
                                         "!!WARNING don't format the texts and don't mention word like this slide, "
                                         "in this presentation")


class BulletPointsGeneratorSignature(dspy.Signature):
    """
    Generate bullet points for a presentation slide based on the main topic and context.
    """
    input: PresentationBulletPointsInput = dspy.InputField()
    next_bullet_point: str = dspy.OutputField(desc="Next bullet point for the slide")


class SpeakerNoteGeneratorSignature(dspy.Signature):
    """
    Generate speaker notes for a presentation slide based on the main topic and context.
    """
    input: PresentationSpeakerNoteInput = dspy.InputField()
    speaker_note: str = dspy.OutputField(desc="Speaker notes for the slide, this is the content user will read out "
                                              "loud to the audience, be simple and clear !!WARNING don't format the "
                                              "texts. Complete the text with the main idea of the slide")
    summary: str = dspy.OutputField(
        desc="Summary of the slide content for context and coherence with previous slides. Complete the text with the "
             "main idea of the slide")


class ImageGenerationPromptGeneratorSignature(dspy.Signature):
    """
    Generate a prompt for image generation based on the slide's content, color scheme, and style.
    """
    input: PresentationImageGenerationPromptInput = dspy.InputField()
    image_generation_prompt: str = dspy.OutputField(
        desc="Prompt for image generation aligned with the slide's content, "
             "to be used to generate images for the slide using generation models"
             "add better image contexts here, like the type of image, the color"
             "scheme, the style, the mood, etc and strictly no text in the image")
