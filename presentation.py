import string
import random
from ai.modules import TitleSubtitleGenerator, ContentGenerator, BulletPointsGenerator, SpeakerNoteAndSummaryGenerator \
    , ImageGenerationPromptGenerator
from models.presentation import PresentationInput, PresentationOutput
from ai.gen_image import generate_image
from util.imageloader import ImageLoader


class PresentationManager(object):
    def __init__(self, presentation_input: PresentationInput, image_loader: ImageLoader):
        self.title_subtitle_generator = TitleSubtitleGenerator()
        self.content_generator = ContentGenerator()
        self.bullet_points_generator = BulletPointsGenerator()
        self.speaker_note_generator = SpeakerNoteAndSummaryGenerator()
        self.image_generation_prompt_generator = ImageGenerationPromptGenerator()
        self.topic = presentation_input.topic
        self.color_scheme: str = presentation_input.color_scheme
        self.target_audience: str = presentation_input.target_audience
        self.total_slides: int = int(presentation_input.total_slides)
        self.current_slide_number: int = int(presentation_input.current_slide_number)
        self.previous_slides_summaries: list[str] = presentation_input.previous_slides_summaries
        self.image_loader = image_loader
        self.output = PresentationOutput(
            title="",
            subtitle="",
            content="",
            bullet_points=[],
            speaker_note="",
            summary="",
            primary_image_url=""
        )

    def generate_next_slide(self):
        if self.current_slide_number >= self.total_slides:
            raise Exception("All slides have been generated.")

        self.current_slide_number += 1
        # Generate the title and subtitle for the slide
        title, subtitle = self.title_subtitle_generator.forward(
            topic=self.topic,
            target_audience=self.target_audience,
            previous_slide_summaries=self.previous_slides_summaries
        )
        self.output.title = title
        self.output.subtitle = subtitle

        # Generate the content for the slide
        content = self.content_generator.forward(
            topic=self.topic,
            target_audience=self.target_audience,
            title=title,
            subtitle=subtitle
        )
        self.output.content = content

        # Generate 3 bullet points for the slide
        bullet_points = []
        for _ in range(3):
            bullet_point = self.bullet_points_generator.forward(
                topic=self.topic,
                target_audience=self.target_audience,
                title=title,
                subtitle=subtitle,
                content=content,
                previous_bullet_points=bullet_points
            )
            bullet_points.append(bullet_point)

        self.output.bullet_points = bullet_points

        # Generate speaker notes and summary for the slide
        speaker_note, summary = self.speaker_note_generator.forward(
            topic=self.topic,
            title=title,
            subtitle=subtitle,
            content=content,
            bullet_points=bullet_points
        )
        self.output.speaker_note = speaker_note
        self.output.summary = summary

        # Generate the image generation prompt for the slide
        image_generation_prompt = self.image_generation_prompt_generator.forward(
            topic=self.topic,
            summary=summary,
            target_audience=self.target_audience,
            color_scheme=self.color_scheme
        )

        # Generate image based on the prompt
        image_path = generate_image(image_generation_prompt)

        # Upload image to cloud storage
        # generate random file name with .webp extension
        file_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
        image_url = self.image_loader.upload_to_s3(image_path, f"{file_name}.webp")

        self.output.primary_image_url = image_url

        return self.output
