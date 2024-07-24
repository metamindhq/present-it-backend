import dspy


class TitleSubtitleGeneratorSignature(dspy.Signature):
    """
    Generate a title and subtitle for a presentation slide based on the main topic and context.
    """
    topic = dspy.InputField(desc="Topic or idea of the presentation")
    target_audience = dspy.InputField(desc="Intended audience for the presentation")
    previous_slide_summaries = dspy.InputField(desc="Summary of the previous slides for context")

    title = dspy.OutputField(desc="Think of a unique, catchy title for the slide with the main idea !!WARNING don't"
                                  "pre format the texts")
    subtitle = dspy.OutputField(desc="Think of a subtitle that complements the title and provides more context "
                                     "!!WARNING don't pre format the texts")


class ContentGeneratorSignature(dspy.Signature):
    """
    Generate content for a presentation slide based on the main topic and context.
    """
    topic = dspy.InputField(desc="Main topic or idea of the presentation")
    target_audience = dspy.InputField(desc="Intended audience for the presentation")
    title = dspy.InputField(desc="Title of the slide")
    subtitle = dspy.InputField(desc="Subtitle of the slide")

    content = dspy.OutputField(desc="Generated content for the slide, to be used before presenting bullet points, "
                                    "!!WARNING don't pre format the texts")


class BulletPointsGeneratorSignature(dspy.Signature):
    """
    Generate bullet points for a presentation slide based on the main topic and context.
    """
    topic = dspy.InputField(desc="Main topic or idea of the presentation")
    target_audience = dspy.InputField(desc="Intended audience for the presentation")
    title = dspy.InputField(desc="Title of the slide")
    subtitle = dspy.InputField(desc="Subtitle of the slide")
    content = dspy.InputField(desc="Content of the slide")
    previous_bullet_points = dspy.InputField(desc="Previous bullet points for context")

    next_bullet_point = dspy.OutputField(desc="Next bullet point for the slide")


class SpeakerNoteGeneratorSignature(dspy.Signature):
    """
    Generate speaker notes for a presentation slide based on the main topic and context.
    """
    topic = dspy.InputField(desc="Main topic or idea of the presentation")
    title = dspy.InputField(desc="Title of the slide")
    subtitle = dspy.InputField(desc="Subtitle of the slide")
    content = dspy.InputField(desc="Content of the slide")
    bullet_points = dspy.InputField(desc="Bullet points for the slide")

    speaker_note = dspy.OutputField(desc="Speaker notes for the slide, this is the content user will read out "
                                         "loud to the audience, be simple and clear !!WARNING don't pre format "
                                         "the texts")
    summary = dspy.OutputField(desc="Summary of the slide content for context and coherence with previous slides")


class ImageGenerationPromptGeneratorSignature(dspy.Signature):
    """
    Generate a prompt for image generation based on the slide's content, color scheme, and style.
    """
    topic = dspy.InputField(desc="Main topic or idea of the presentation")
    summary = dspy.InputField(desc="Summary of the slide content for context and coherence with previous slides")
    target_audience = dspy.InputField(desc="Intended audience for the presentation")
    color_scheme = dspy.InputField(desc="Desired color scheme with specific color descriptions")

    image_generation_prompt = dspy.OutputField(desc="Prompt for image generation aligned with the slide's content, "
                                                    "to be used to generate images for the slide using generation models"
                                                    "add better image contexts here, like the type of image, the color "
                                                    "scheme, the style, the mood, etc"
                                               )
