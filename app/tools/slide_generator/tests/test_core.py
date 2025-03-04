import pytest
from unittest.mock import patch, MagicMock, Mock
import os
import sys
from app.services.schemas import SlideGeneratorInput
from app.api.error_utilities import LoaderError, ToolExecutorError
from app.tools.slide_generator.core import executor
from app.tools.slide_generator.tools import SlideGenerator, SlidePresentation, Slide
from langchain_core.documents import Document

# Test SlideGenerator tools.py

@pytest.fixture
def mock_args():
    return SlideGeneratorInput(
        slides_titles=["Introduction to Python", "Variables and Data Types", "Control Flow"],
        instructional_level="beginner",
        topic="Python Basics",
        lang="en"
    )

@pytest.fixture
def mock_model():
    mock = MagicMock()
    return mock

@pytest.fixture
def mock_parser():
    mock = MagicMock()
    mock.get_format_instructions.return_value = "JSON instructions"
    return mock

@pytest.fixture
def mock_vectorstore_class():
    mock = MagicMock()
    return mock

class TestSlideGenerator:
    
    def test_init(self, mock_args):
        generator = SlideGenerator(args=mock_args)
        assert generator.args == mock_args
        assert generator.vectorstore is None
        assert generator.retriever is None
        assert generator.runner is None
        
    @patch('app.tools.slide_generator.tools.PromptTemplate')
    def test_compile_with_context(self, mock_prompt_template, mock_args, mock_model, mock_parser):
        mock_prompt_template.return_value = "formatted_prompt"
        generator = SlideGenerator(
            args=mock_args, 
            model=mock_model, 
            parser=mock_parser
        )
        
        chain = generator.compile_with_context()
        
        mock_prompt_template.assert_called_once()
        assert chain is not None
        
    def test_generate_slides(self, mock_args, mock_model, mock_parser, mock_vectorstore_class):
        # Create mock slides to return
        mock_slides = {
            "slides": [
                {
                    "title": "Introduction to Python",
                    "template": "sectionHeader",
                    "content": "A beginner's guide to Python programming"
                },
                {
                    "title": "Variables and Data Types",
                    "template": "titleAndBody",
                    "content": "Learn about different data types in Python"
                }
            ]
        }
        
        # Create a mock chain that will be returned by compile_with_context
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = mock_slides
        
        generator = SlideGenerator(
            args=mock_args, 
            model=mock_model, 
            parser=mock_parser,
            vectorstore_class=mock_vectorstore_class
        )
        
        # Mock the compile_with_context method
        generator.compile_with_context = MagicMock(return_value=mock_chain)
        
        result = generator.generate_slides()
        
        generator.compile_with_context.assert_called_once()
        mock_chain.invoke.assert_called_once()
        assert result == mock_slides

# Test executor core.py

@pytest.fixture
def mock_slide_generator():
    generator = MagicMock()
    mock_slides = {
        "slides": [
            {
                "title": "Introduction to Python",
                "template": "sectionHeader",
                "content": "A beginner's guide to Python programming"
            },
            {
                "title": "Variables and Data Types",
                "template": "titleAndBody",
                "content": "Learn about different data types in Python"
            }
        ]
    }
    generator.generate_slides.return_value = mock_slides
    return generator

class TestSlideGeneratorExecutor:
    
    @patch('app.tools.slide_generator.core.SlideGenerator')
    def test_executor_success(self, mock_generator_class, mock_slide_generator):
        mock_generator_class.return_value = mock_slide_generator
        
        result = executor(
            slides_titles=["Introduction to Python", "Variables and Data Types"],
            topic="Python Basics",
            instructional_level="beginner",
            lang="en",
            verbose=True
        )
        
        mock_generator_class.assert_called_once()
        mock_slide_generator.generate_slides.assert_called_once()
        assert result == mock_slide_generator.generate_slides.return_value
        
    @patch('app.tools.slide_generator.core.SlideGenerator')
    def test_executor_loader_error(self, mock_generator_class):
        mock_generator_class.side_effect = LoaderError("Error loading slides")
        
        with pytest.raises(ToolExecutorError):
            executor(
                slides_titles=["Introduction to Python", "Variables and Data Types"],
                topic="Python Basics",
                instructional_level="beginner",
                lang="en"
            )
        
    @patch('app.tools.slide_generator.core.SlideGenerator')
    def test_executor_generic_error(self, mock_generator_class):
        mock_generator_class.side_effect = Exception("Generic error")
        
        with pytest.raises(ValueError):
            executor(
                slides_titles=["Introduction to Python", "Variables and Data Types"],
                topic="Python Basics",
                instructional_level="beginner",
                lang="en"
            )
        
    def test_executor_missing_required_inputs(self):
        result = executor(
            slides_titles=None,
            topic="Python Basics",
            instructional_level="beginner",
            lang="en"
        )
        
        # Since the missing input is handled but doesn't raise an exception, 
        # we expect the function to continue and return the result
        assert result is not None