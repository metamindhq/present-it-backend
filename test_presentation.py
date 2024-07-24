import pytest
from unittest.mock import Mock, patch
from presentation import PresentationManager
from models.presentation import PresentationInput, PresentationOutput
from util.imageloader import ImageLoader

@pytest.fixture
def mock_image_loader():
    return Mock(spec=ImageLoader)

@pytest.fixture
def presentation_input():
    return PresentationInput(
        topic="Artificial Intelligence",
        color_scheme="Blue and White",
        target_audience="Tech enthusiasts",
        total_slides=5,
        current_slide_number=0,
        previous_slides_summaries=[]
    )

def test_generate_next_slide(presentation_input, mock_image_loader):
    # Create mock objects for all the generator classes
    mock_title_subtitle_gen = Mock()
    mock_content_gen = Mock()
    mock_bullet_points_gen = Mock()
    mock_speaker_note_gen = Mock()
    mock_image_prompt_gen = Mock()

    # Set up mock returns for each .forward() call
    mock_title_subtitle_gen.forward.return_value = ("AI Revolution", "Transforming Our World")
    mock_content_gen.forward.return_value = "AI is changing every aspect of our lives..."
    mock_bullet_points_gen.forward.side_effect = [
        "Machine Learning applications",
        "Natural Language Processing advancements",
        "AI in healthcare"
    ]
    mock_speaker_note_gen.forward.return_value = (
        "Today, we'll explore how AI is revolutionizing various industries...",
        "Summary of AI's impact on different sectors"
    )
    mock_image_prompt_gen.forward.return_value = "A futuristic cityscape with AI-powered technology"

    # Mock the generate_image function
    mock_generate_image = Mock(return_value="/tmp/generated_image.webp")

    # Set up the mock for image upload
    mock_image_loader.upload_to_s3.return_value = "https://example.com/image.webp"

    # Create PresentationManager instance with mocked dependencies
    with patch('presentation.TitleSubtitleGenerator', return_value=mock_title_subtitle_gen), \
         patch('presentation.ContentGenerator', return_value=mock_content_gen), \
         patch('presentation.BulletPointsGenerator', return_value=mock_bullet_points_gen), \
         patch('presentation.SpeakerNoteAndSummaryGenerator', return_value=mock_speaker_note_gen), \
         patch('presentation.ImageGenerationPromptGenerator', return_value=mock_image_prompt_gen), \
         patch('presentation.generate_image', mock_generate_image):

        manager = PresentationManager(presentation_input, mock_image_loader)

        # Generate next slide
        result = manager.generate_next_slide()

    # Assertions
    assert isinstance(result, PresentationOutput)
    assert result.title == "AI Revolution"
    assert result.subtitle == "Transforming Our World"
    assert result.content == "AI is changing every aspect of our lives..."
    assert result.bullet_points == [
        "Machine Learning applications",
        "Natural Language Processing advancements",
        "AI in healthcare"
    ]
    assert result.speaker_note == "Today, we'll explore how AI is revolutionizing various industries..."
    assert result.summary == "Summary of AI's impact on different sectors"
    assert result.primary_image_url == "https://example.com/image.webp"

    # Verify method calls
    mock_title_subtitle_gen.forward.assert_called_once()
    mock_content_gen.forward.assert_called_once()
    assert mock_bullet_points_gen.forward.call_count == 3
    mock_speaker_note_gen.forward.assert_called_once()
    mock_image_prompt_gen.forward.assert_called_once()
    mock_generate_image.assert_called_once()
    mock_image_loader.upload_to_s3.assert_called_once()

    # Check if current_slide_number is incremented
    assert manager.current_slide_number == 1

@pytest.mark.parametrize("current_slide,total_slides", [(4, 5), (5, 5)])
def test_generate_next_slide_limit(current_slide, total_slides, mock_image_loader):
    input_data = PresentationInput(
        topic="Test Topic",
        color_scheme="Red and Black",
        target_audience="General public",
        total_slides=total_slides,
        current_slide_number=current_slide,
        previous_slides_summaries=[]
    )

    # Create mock objects for all the generator classes
    mock_title_subtitle_gen = Mock()
    mock_content_gen = Mock()
    mock_bullet_points_gen = Mock()
    mock_speaker_note_gen = Mock()
    mock_image_prompt_gen = Mock()

    # Set up basic mock returns (these won't be used in the limit test, but are needed to initialize)
    mock_title_subtitle_gen.forward.return_value = ("Title", "Subtitle")
    mock_content_gen.forward.return_value = "Content"
    mock_bullet_points_gen.forward.return_value = "Bullet point"
    mock_speaker_note_gen.forward.return_value = ("Speaker note", "Summary")
    mock_image_prompt_gen.forward.return_value = "Image prompt"

    # Mock the generate_image function
    mock_generate_image = Mock(return_value="/tmp/generated_image.webp")

    # Create PresentationManager instance with mocked dependencies
    with patch('presentation.TitleSubtitleGenerator', return_value=mock_title_subtitle_gen), \
         patch('presentation.ContentGenerator', return_value=mock_content_gen), \
         patch('presentation.BulletPointsGenerator', return_value=mock_bullet_points_gen), \
         patch('presentation.SpeakerNoteAndSummaryGenerator', return_value=mock_speaker_note_gen), \
         patch('presentation.ImageGenerationPromptGenerator', return_value=mock_image_prompt_gen), \
         patch('presentation.generate_image', mock_generate_image):

        manager = PresentationManager(input_data, mock_image_loader)

        if current_slide < total_slides:
            result = manager.generate_next_slide()
            assert isinstance(result, PresentationOutput)
            assert manager.current_slide_number == total_slides
        else:
            with pytest.raises(Exception, match="All slides have been generated."):
                manager.generate_next_slide()