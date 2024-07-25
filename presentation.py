import string
import random
from ai.modules import TitleSubtitleGenerator, ContentGenerator, BulletPointsGenerator, SpeakerNoteAndSummaryGenerator \
    , ImageGenerationPromptGenerator
from models.presentation import PresentationInput, PresentationOutput
from models.image import ImageGenerationInput, ImageGenerationOutput
from ai.gen_image import generate_image
from util.imageloader import ImageLoader


class PresentationManager(object):
    def __init__(self, image_loader: ImageLoader):
        self.title_subtitle_generator = TitleSubtitleGenerator()
        self.content_generator = ContentGenerator()
        self.bullet_points_generator = BulletPointsGenerator()
        self.speaker_note_generator = SpeakerNoteAndSummaryGenerator()
        self.image_generation_prompt_generator = ImageGenerationPromptGenerator()
        self.image_loader = image_loader

    def generate_next_slide(self, presentation_input: PresentationInput) -> PresentationOutput:
        output = PresentationOutput(
            title="",
            subtitle="",
            content="",
            bullet_points=[],
            speaker_note="",
            summary="",
            image_generation_prompt=""
        )
        if presentation_input.current_slide_number >= presentation_input.total_slides:
            raise Exception("All slides have been generated.")

        presentation_input.current_slide_number += 1
        # Generate the title and subtitle for the slide
        title, subtitle = self.title_subtitle_generator.forward(
            topic=presentation_input.topic,
            target_audience=presentation_input.target_audience,
            previous_slide_summaries=presentation_input.previous_slides_summaries
        )
        output.title = title
        output.subtitle = subtitle

        # Generate the content for the slide
        content = self.content_generator.forward(
            topic=presentation_input.topic,
            target_audience=presentation_input.target_audience,
            title=title,
            subtitle=subtitle
        )
        output.content = content

        # Generate 3 bullet points for the slide
        bullet_points = []
        for _ in range(3):
            bullet_point = self.bullet_points_generator.forward(
                topic=presentation_input.topic,
                target_audience=presentation_input.target_audience,
                title=title,
                subtitle=subtitle,
                content=content,
                previous_bullet_points=bullet_points
            )
            bullet_points.append(bullet_point)

        output.bullet_points = bullet_points

        # Generate speaker notes and summary for the slide
        speaker_note, summary = self.speaker_note_generator.forward(
            topic=presentation_input.topic,
            title=title,
            subtitle=subtitle,
            content=content,
            bullet_points=bullet_points
        )
        output.speaker_note = speaker_note
        output.summary = summary

        # Generate the image generation prompt for the slide
        image_generation_prompt = self.image_generation_prompt_generator.forward(
            topic=presentation_input.topic,
            summary=summary,
            target_audience=presentation_input.target_audience,
            color_scheme=presentation_input.color_scheme
        )

        # Generate image based on the prompt
        output.image_generation_prompt = image_generation_prompt

        return output

    def generate_image_by_prompt(self, image_generation_prompt: ImageGenerationInput) -> ImageGenerationOutput:
        image_path = generate_image(image_generation_prompt.image_generation_prompt)
        file_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
        image_url = self.image_loader.upload_to_gcp_object_store(image_path, f"images/{file_name}.webp")
        return ImageGenerationOutput(
            image_generation_prompt=image_generation_prompt.image_generation_prompt,
            image_public_url=image_url
        )
