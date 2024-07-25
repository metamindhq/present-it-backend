import dspy

from ai.signatures import TitleSubtitleGeneratorSignature, ContentGeneratorSignature, BulletPointsGeneratorSignature, \
    SpeakerNoteGeneratorSignature, ImageGenerationPromptGeneratorSignature


class TitleSubtitleGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.ChainOfThought(TitleSubtitleGeneratorSignature)

    def forward(self, topic, target_audience, previous_slide_summaries=None):
        previous_summaries = None
        if previous_slide_summaries:
            # Convert the list of summaries to a string
            previous_summaries = ",".join(previous_slide_summaries)
        output = self.gen(topic=topic, target_audience=target_audience, previous_slide_summaries=previous_summaries)
        return output.title, output.subtitle


class ContentGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.Predict(ContentGeneratorSignature)

    def forward(self, topic, target_audience, title, subtitle):
        output = self.gen(topic=topic, target_audience=target_audience, title=title, subtitle=subtitle)
        return output.content


class BulletPointsGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.ChainOfThought(BulletPointsGeneratorSignature)

    def forward(self, topic, target_audience, title, subtitle, content, previous_bullet_points=None):
        prev_bullet_points = None
        if previous_bullet_points:
            # Convert the list of summaries to a string
            prev_bullet_points = ",".join(previous_bullet_points)
        output = self.gen(topic=topic, target_audience=target_audience, title=title, subtitle=subtitle, content=content,
                          previous_bullet_points=prev_bullet_points)
        return output.next_bullet_point


class SpeakerNoteAndSummaryGenerator(dspy.Module):
    """
    Generate speaker notes for a presentation slide based on the main topic and context.
    """

    def __init__(self):
        super().__init__()
        self.gen = dspy.Predict(SpeakerNoteGeneratorSignature)

    def forward(self, topic, title, subtitle, content, bullet_points):
        output = self.gen(topic=topic, title=title, subtitle=subtitle, content=content,
                          bullet_points=",".join(bullet_points))
        return output.speaker_note, output.summary


class ImageGenerationPromptGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gen = dspy.ChainOfThought(ImageGenerationPromptGeneratorSignature)

    def forward(self, topic, summary, target_audience, color_scheme):
        output = self.gen(topic=topic, summary=summary, target_audience=target_audience, color_scheme=color_scheme)
        return output.image_generation_prompt
