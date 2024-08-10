import json
import string
import random

from openai import OpenAI
import weave

from ai.gen_prompt import get_dynamic_slide_gen_system_message
from ai.modules import TitleSubtitleGenerator, ContentGenerator, BulletPointsGenerator, SpeakerNoteAndSummaryGenerator \
    , ImageGenerationPromptGenerator
from models.presentation import (PresentationTitleSubtitleInput, PresentationContentInput,
                                 PresentationBulletPointsInput,
                                 PresentationSpeakerNoteInput, PresentationImageGenerationPromptInput)

from models.presentation import PresentationInput, PresentationOutput
from models.image import ImageGenerationInput, ImageGenerationOutput
from ai.gen_image import generate_image, gen_image_replicate
from util.imageloader import ImageLoader


@weave.op()
def generate_next_slide_using_openai(presentation_input: PresentationInput, client: OpenAI) -> PresentationOutput:
    system_prompt = get_dynamic_slide_gen_system_message(
        genre=presentation_input.target_audience,
        theme=presentation_input.color_scheme,
        summary=presentation_input.previous_slides_summaries,
        offset=presentation_input.current_slide_number,
        total_slides=presentation_input.total_slides
    )
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": presentation_input.topic}
        ],
        temperature=0.5,
        max_tokens=1024,
        top_p=0.5,
        frequency_penalty=2,
        presence_penalty=2,
        response_format={
            "type": "json_object"
        }
    )
    resp = json.loads(completion.choices[0].message.content)
    output = PresentationOutput(
        title=resp['title'],
        subtitle=resp['subtitle'],
        content=resp['content'],
        bullet_points=resp['bullet_points'],
        speaker_note=resp['speaker_note'],
        summary=resp['summary'],
        image_generation_prompt=resp['image_generation_prompt']
    )
    return output


class PresentationManager(object):
    def __init__(self, image_loader: ImageLoader):
        self.title_subtitle_generator = TitleSubtitleGenerator()
        self.content_generator = ContentGenerator()
        self.bullet_points_generator = BulletPointsGenerator()
        self.speaker_note_generator = SpeakerNoteAndSummaryGenerator()
        self.image_generation_prompt_generator = ImageGenerationPromptGenerator()
        self.image_loader = image_loader

    @weave.op()
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
        title_subtitle_output = self.title_subtitle_generator.forward(
            PresentationTitleSubtitleInput(
                topic=presentation_input.topic,
                target_audience=presentation_input.target_audience,
                current_slide_number=str(presentation_input.current_slide_number),
                total_slides=str(presentation_input.total_slides),
                previous_slide_summaries=presentation_input.previous_slides_summaries
            )
        )
        output.title = title_subtitle_output.title
        output.subtitle = title_subtitle_output.subtitle

        # Generate the content for the slide
        content_output = self.content_generator.forward(
            PresentationContentInput(
                topic=presentation_input.topic,
                target_audience=presentation_input.target_audience,
                current_slide_number=str(presentation_input.current_slide_number),
                total_slides=str(presentation_input.total_slides),
                title=output.title,
                subtitle=output.subtitle
            )
        )
        output.content = content_output.content

        # Generate 3 bullet points for the slide
        bullet_points: str = ""
        bullet_points_list = []
        for _ in range(3):
            bullet_point_output = self.bullet_points_generator.forward(
                PresentationBulletPointsInput(
                    topic=presentation_input.topic,
                    target_audience=presentation_input.target_audience,
                    title=output.title,
                    subtitle=output.subtitle,
                    content=output.content,
                    previous_bullet_points=bullet_points
                )
            )
            bullet_points_list.append(bullet_point_output.next_bullet_point)
            bullet_points += bullet_point_output.next_bullet_point + ","

        output.bullet_points = bullet_points_list

        # Generate speaker notes and summary for the slide
        speaker_note_output = self.speaker_note_generator.forward(
            PresentationSpeakerNoteInput(
                topic=presentation_input.topic,
                target_audience=presentation_input.target_audience,
                title=output.title,
                subtitle=output.subtitle,
                content=output.content,
                bullet_points=bullet_points,
                summaries=presentation_input.previous_slides_summaries,
                current_slide_number=str(presentation_input.current_slide_number),
                total_slides=str(presentation_input.total_slides)
            )
        )
        output.speaker_note = speaker_note_output.speaker_note
        output.summary = speaker_note_output.summary

        # Generate the image generation prompt for the slide
        image_generation_prompt_output = self.image_generation_prompt_generator.forward(
            PresentationImageGenerationPromptInput(
                topic=presentation_input.topic,
                target_audience=presentation_input.target_audience,
                summary=output.summary,
                color_scheme=presentation_input.color_scheme
            )
        )

        # Generate image based on the prompt
        output.image_generation_prompt = image_generation_prompt_output.image_generation_prompt

        return output

    def generate_image_by_prompt(self, image_generation_prompt: ImageGenerationInput) -> ImageGenerationOutput:
        image_url = gen_image_replicate(image_generation_prompt.image_generation_prompt)
        file_name = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
        # image_url = self.image_loader.upload_to_gcp_object_store(image_path, f"images/{file_name}.webp")
        return ImageGenerationOutput(
            image_generation_prompt=image_generation_prompt.image_generation_prompt,
            image_public_url=image_url
        )
