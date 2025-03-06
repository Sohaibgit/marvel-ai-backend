import pytest
from app.tools.presentation_generator.slide_generator.core import executor,SlideGeneratorInput
from unittest.mock import patch, MagicMock, Mock
from app.tools.presentation_generator.slide_generator.tools import SlideGenerator, Slide,SlidePresentation

@pytest.fixture
def mock_slide_data():
    return {
        "slides": [
            {
                "title": "Introduction to Python",
                "template": "titleAndBullets",
                "content": ["Python is a programming language"]
            },
            {
                "title": "Basic Syntax",
                "template": "titleBody",
                "content": "Python syntax is simple"
            }
        ]
    }
@pytest.fixture
def mock_args():
    return SlideGeneratorInput(
        slides_titles=["Intro", "Details"],
        topic="Data Science",
        instructional_level="Intermediate",
        lang="en"
    )
# @pytest.fixture
# def mock_slide_generator():
#     with patch("app.tools.presentation_generator.slide_generator.tools.GoogleGenerativeAI", autospec=True) as mock_model, \
#          patch("app.tools.presentation_generator.slide_generator.tools.GoogleGenerativeAIEmbeddings", autospec=True) as mock_embeddings, \
#          patch("app.tools.presentation_generator.slide_generator.tools.JsonOutputParser", autospec=True) as mock_parser, \
#          patch("app.tools.presentation_generator.slide_generator.tools.read_text_file", return_value="Mocked Prompt") as mock_read_text_file, \
#          patch("app.tools.presentation_generator.slide_generator.tools.Chroma", autospec=True) as mock_chroma:

#         # Create mock objects for the dependencies
#         mock_model_instance = mock_model.return_value
#         mock_embeddings_instance = mock_embeddings.return_value
#         mock_parser_instance = mock_parser.return_value
#         mock_chroma_instance = mock_chroma.return_value

#         # Create a mock SlideGenerator instance
#         slide_generator = SlideGenerator()

#         # Override attributes with mocks
#         slide_generator.model = mock_model_instance
#         slide_generator.embedding_model = mock_embeddings_instance
#         slide_generator.parser = mock_parser_instance
#         slide_generator.prompt = "Mocked Prompt"
#         slide_generator.vectorstore_class = mock_chroma_instance

#         yield slide_generator

@pytest.fixture
def mock_slide_generator():
    """Mock SlideGenerator instead of instantiating it."""
    with patch("app.tools.presentation_generator.slide_generator.tools.SlideGenerator") as MockSlideGenerator:
        instance = MockSlideGenerator.return_value
        instance.validate_slides_content.return_value = {
            "topic_coverage": 80,
            "template_requirements_met": True,
            "garbage_coverage_percentage": 0,
            "valid": True
        }
        yield instance
#passsing test
def test_executor(mock_slide_data):
    slides_titles = ["Introduction to Python", "Basic Syntax"]
    topic = "Python Programming"
    instructional_level = "Beginner"
    lang = "en"
    verbose = False


    # Create a mock instance of SlideGenerator
    mock_slide_generator = MagicMock()
    mock_slide_generator.generate_slides.return_value = mock_slide_data

    # Patch SlideGenerator to return the mock instance
    with patch("app.tools.presentation_generator.slide_generator.core.SlideGenerator", return_value=mock_slide_generator):
        result = executor(slides_titles, topic, instructional_level, lang, verbose)
    # Assertions
    assert result == mock_slide_data
    mock_slide_generator.generate_slides.assert_called_once() 
   # Ensure the function was called once

def test_executor_missing_inputs():
    """Test the executor function with missing required inputs."""
    with pytest.raises(ValueError, match="Missing required inputs"):
        executor(
            slides_titles=[],
            topic="",
            instructional_level="",
            lang="en"
        )
@patch("app.tools.presentation_generator.slide_generator.tools.SlideGenerator.generate_slides")
@patch("google.auth.default")
def test_executor_loader_error(mock_auth,mock_generate_slides):
    mock_auth.return_value=(MagicMock(),"fake-project-id")
    from app.api.error_utilities import LoaderError
    mock_generate_slides.side_effect = LoaderError("Error in Slide Generator Pipeline")
    with pytest.raises(Exception) as exc_info:
        executor(slides_titles=["Intro"], topic="AI", instructional_level="Intermediate", lang="en")
    assert "Error in Slide Generator Pipeline" in str(exc_info.value)

@patch("app.tools.presentation_generator.slide_generator.tools.SlideGenerator.generate_slides")
@patch("google.auth.default")
def test_executor_unexpected_error(mock_auth,mock_generate_slides):
    mock_auth.return_value=(MagicMock(),"fake-project-id")
    mock_generate_slides.side_effect = Exception("Unexpected error occurred")
    with pytest.raises(ValueError, match="Error in executor: Unexpected error occurred"):
        executor(slides_titles=["Intro"], topic="AI", instructional_level="Intermediate", lang="en")

def test_slide_generator(mock_args):    
    with patch.object(SlideGenerator, "__init__", lambda self, *args, **kwargs: None):
        slide_generator = SlideGenerator()
        slide_generator.args = mock_args
        slide_generator.prompt = "Mocked Prompt"
        slide_generator.model = MagicMock()
        slide_generator.embedding_model = MagicMock()
        slide_generator.parser = MagicMock()
        slide_generator.vectorstore_class = MagicMock()
    assert slide_generator.prompt == "Mocked Prompt"
    assert slide_generator.args == mock_args
    assert slide_generator.model is not None
    assert slide_generator.embedding_model is not None
    assert slide_generator.parser is not None
    assert slide_generator.vectorstore_class is not None

@patch("app.tools.presentation_generator.slide_generator.tools.SlideGenerator.validate_slides_content")
@patch("google.auth.default")
def test_validate_slides_content(mock_auth,mock_validate, mock_slide_generator, mock_slide_data):
    mock_auth.return_value=(MagicMock(),"fake-project-id")
    mock_validate.return_value = {
        "topic_coverage": 80,
        "template_requirements_met": True,
        "garbage_coverage_percentage": 0,
        "valid": True
    }
    validation_result = mock_slide_generator.validate_slides_content(mock_slide_data, "Python", "Beginner")
    assert validation_result["valid"] is True
    assert validation_result["topic_coverage"] >= 70


def test_validate_slides_content_with_garbage(mock_slide_generator):
        # Test data - has markdown remnants
        test_instance =mock_slide_generator
        test_instance
        topic = "Biology"
        input = {
            "slides": [
                {
                    "template": "title",
                    "content": "Introduction to *Biology*"
                },
                {
                    "template": "twoColumn",
                    "content": "Cell structure and\nfunction"
                },
                {
                    "template": "basic",
                    "content": ["DNA `replication`", "Protein synthesis"]
                }
            ]
        }
        
        result = test_instance.validate_slides_content(input, topic)
        
        assert result["topic_coverage"] == 33.33333333333333  # 1 out of 3 slides has the topic keyword
        assert result["template_requirements_met"] is True
        assert result["garbage_coverage_percentage"] == 100.0  # All slides have markdown or newlines
        assert result["valid"] is False  # Has garbage content


def test_validate_slides_content_empty_slides(mock_slide_generator):
        # Test with empty slides array
        test_instance = MagicMock()
        topic = "Chemistry"
        response = {
            "slides": []
        }
        
        with pytest.raises(ValueError, match="No slides found in the response"):
            test_instance.validate_slides_content(response, topic)



def test_slide_generator_compile_with_context(mock_args,mock_slide_generator):
    """Test compilation of pipeline."""
    args = mock_args
    test_instance = mock_slide_generator
    test_instance.args = args
    
    chain = test_instance.compile_with_context()
    
    assert chain is not None



def test_slide_model():
    """Test the Slide Pydantic model."""
    slide = Slide(
        title="Introduction",
        template="titleAndBullets",
        content=["Key Point 1", "Key Point 2"]
    )
    
    assert slide.title == "Introduction"
    assert slide.template == "titleAndBullets"
    assert slide.content == ["Key Point 1", "Key Point 2"]

def test_slide_presentation_model():
    """Test the SlidePresentation Pydantic model."""
    slides = [
        Slide(title="Intro", template="titleAndBody", content="Overview"),
        Slide(title="Details", template="twoColumn", content={"left": "Content1", "right": "Content2"})
    ]
    
    presentation = SlidePresentation(slides=slides)
    
    assert len(presentation.slides) == 2
    assert all(isinstance(slide, Slide) for slide in presentation.slides)