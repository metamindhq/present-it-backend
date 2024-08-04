import dspy

from ai.signatures import TitleSubtitleGeneratorSignature, ContentGeneratorSignature, BulletPointsGeneratorSignature, \
    SpeakerNoteGeneratorSignature, ImageGenerationPromptGeneratorSignature, SummaryGeneratorSignature
from models.presentation import (PresentationTitleSubtitleInput, PresentationContentInput, PresentationBulletPointsInput \
    , PresentationSpeakerNoteInput, PresentationImageGenerationPromptInput, PresentationTitleSubtitleOutput \
    , PresentationContentOutput, PresentationBulletPointsOutput, PresentationSpeakerNoteOutput,
                                 PresentationImageGenerationPromptOutput)


class TitleSubtitleGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.Predict(TitleSubtitleGeneratorSignature)

    def forward(self, presentation_input: PresentationTitleSubtitleInput) -> PresentationTitleSubtitleOutput:
        gen = self.gen(input=presentation_input)
        return PresentationTitleSubtitleOutput(
            title=gen.title,
            subtitle=gen.subtitle
        )


class ContentGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.Predict(ContentGeneratorSignature)

    def forward(self, content_generator_input: PresentationContentInput) -> PresentationContentOutput:
        gen = self.gen(input=content_generator_input)
        return PresentationContentOutput(content=gen.content)


class BulletPointsGenerator(dspy.Module):
    """
    Generate bullet points for a presentation slide based on the main topic and context.
    """
    def __init__(self):
        super().__init__()
        self.gen = dspy.Predict(BulletPointsGeneratorSignature)

    def forward(self, bullet_points_generator_input: PresentationBulletPointsInput) -> PresentationBulletPointsOutput:
        gen = self.gen(input=bullet_points_generator_input)
        return PresentationBulletPointsOutput(next_bullet_point=gen.next_bullet_point)


class SpeakerNoteAndSummaryGenerator(dspy.Module):
    """
    Generate speaker notes for a presentation slide based on the main topic and context.
    """

    def __init__(self):
        super().__init__()
        self.speaker_note = dspy.Predict(SpeakerNoteGeneratorSignature)
        self.summary = dspy.Predict(SummaryGeneratorSignature)

    def forward(self, speaker_note_input: PresentationSpeakerNoteInput) -> PresentationSpeakerNoteOutput:
        speaker_note = self.speaker_note(input=speaker_note_input)
        summary = self.summary(input=speaker_note_input)

        return PresentationSpeakerNoteOutput(
            speaker_note=speaker_note.speaker_note,
            summary=summary.summary
        )


class ImageGenerationPromptGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.Predict(ImageGenerationPromptGeneratorSignature)

    def forward(self,
                image_generation_prompt_input: PresentationImageGenerationPromptInput) -> PresentationImageGenerationPromptOutput:
        gen = self.gen(input=image_generation_prompt_input)
        return PresentationImageGenerationPromptOutput(image_generation_prompt=gen.image_generation_prompt)
