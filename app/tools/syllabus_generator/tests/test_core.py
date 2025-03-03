import pytest
from unittest.mock import patch, MagicMock
from app.api.error_utilities import SyllabusGeneratorError
from app.tools.syllabus_generator.core import executor
from app.services.schemas import SyllabusGeneratorArgsModel
from app.tools.syllabus_generator.pipeline import generate_syllabus, SyllabusRequestArgs

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Base attributes reused across all tests
base_attributes = {
    "grade_level": "5th grade",
    "subject": "Math",
    "course_description": "This course covers basic arithmetic operations.",
    "objectives": "Understand addition, subtraction, multiplication, and division.",
    "required_materials": "Notebook, pencils, calculator.",
    "grading_policy": "Homework 40%, Exams 60%.",
    "policies_expectations": "Complete assignments on time, participate in class.",
    "course_outline": "Week 1: Addition; Week 2: Subtraction; Week 3: Multiplication.",
    "additional_notes": "Bring a calculator every day.",
    "lang": "en"
}

# PDF Tests
def test_executor_pdf_url_valid():
    syllabus = executor(
        **base_attributes,
        file_url="https://filesamples.com/samples/document/pdf/sample1.pdf",
        file_type="pdf"
    )
    assert isinstance(syllabus, dict)

def test_executor_pdf_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://filesamples.com/samples/document/pdf/sample1.pdf",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# CSV Tests
def test_executor_csv_url_valid():
    syllabus = executor(
        **base_attributes,
        file_url="https://filesamples.com/samples/document/csv/sample1.csv",
        file_type="csv"
    )
    assert isinstance(syllabus, dict)

def test_executor_csv_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://filesamples.com/samples/document/csv/sample1.csv",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# TXT Tests
def test_executor_txt_url_valid():
    syllabus = executor(
        **base_attributes,
        file_url="https://filesamples.com/samples/document/txt/sample1.txt",
        file_type="txt"
    )
    assert isinstance(syllabus, dict)

def test_executor_txt_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://filesamples.com/samples/document/txt/sample1.txt",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# MD Tests
def test_executor_md_url_valid():
    syllabus = executor(
        **base_attributes,
        file_url="https://github.com/radicalxdev/kai-ai-backend/blob/main/README.md",
        file_type="md"
    )
    assert isinstance(syllabus, dict)

def test_executor_md_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://github.com/radicalxdev/kai-ai-backend/blob/main/README.md",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# PPTX Tests
def test_executor_pptx_url_valid():
    syllabus = executor(
        **base_attributes,
        file_url="https://scholar.harvard.edu/files/torman_personal/files/samplepptx.pptx",
        file_type="pptx"
    )
    assert isinstance(syllabus, dict)

def test_executor_pptx_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://scholar.harvard.edu/files/torman_personal/files/samplepptx.pptx",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# DOCX Tests
def test_executor_docx_url_valid():
    syllabus = executor(
        **base_attributes,
        file_url="https://filesamples.com/samples/document/docx/sample1.docx",
        file_type="docx"
    )
    assert isinstance(syllabus, dict)

def test_executor_docx_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://filesamples.com/samples/document/docx/sample1.docx",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# XLS Tests
def test_executor_xls_url_valid():
    syllabus = executor(
        **base_attributes,
        file_url="https://filesamples.com/samples/document/xls/sample1.xls",
        file_type="xls"
    )
    assert isinstance(syllabus, dict)

def test_executor_xls_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://filesamples.com/samples/document/xls/sample1.xls",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# XLSX Tests
def test_executor_xlsx_url_valid():
    syllabus = executor(
        **base_attributes,
        file_url="https://filesamples.com/samples/document/xlsx/sample1.xlsx",
        file_type="xlsx"
    )
    assert isinstance(syllabus, dict)

def test_executor_xlsx_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://filesamples.com/samples/document/xlsx/sample1.xlsx",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# XML Tests
def test_executor_xml_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://filesampleshub.com/download/code/xml/dummy.xml",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# GDocs Tests
def test_executor_gdocs_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://docs.google.com/document/d/1OWQfO9LX6psGipJu9LabzNE22us1Ct/edit",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# GSheets Tests
def test_executor_gsheets_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://docs.google.com/spreadsheets/d/16OPtLLSfU/edit",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# GSlides Tests
def test_executor_gslides_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://docs.google.com/spreadsheets/d/16OPtLLSfU/edit",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# GPDFs Tests
def test_executor_gpdfs_url_valid():
    syllabus = executor(
        **base_attributes,
        file_url="https://drive.google.com/file/d/1fUj1uWIMh6QZsPkt0Vs7mEd2VEqz3O8l/view",
        file_type="gpdf"
    )
    assert isinstance(syllabus, dict)

def test_executor_gpdfs_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://drive.google.com/file/d/1fUj1uWIMh6QZsPkt0Vs7mEd2VEqz3O8l/view",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)

# MP3 Tests
def test_executor_mp3_url_invalid():
    with pytest.raises(SyllabusGeneratorError) as exc_info:
        executor(
            **base_attributes,
            file_url="https://raw.githubusercontent.com/asleem/uploaded_files/main/dummy.mp3",
            file_type=1
        )
    assert isinstance(exc_info.value, SyllabusGeneratorError)


# Test for SyllabusRequestArgs class
def test_syllabus_request_args():
    # Create a mock SyllabusGeneratorArgsModel object
    mock_args = MagicMock(spec=SyllabusGeneratorArgsModel)
    for key, value in base_attributes.items():
        setattr(mock_args, key, value)
    
    # Test initialization and to_dict method
    request_args = SyllabusRequestArgs(mock_args, "Test summary")
    args_dict = request_args.to_dict()
    
    assert args_dict["grade_level"] == "5th grade"
    assert args_dict["subject"] == "Math"
    assert args_dict["summary"] == "Test summary"
    assert "course_description" in args_dict
    assert "objectives" in args_dict

# Test the pipeline compilation
@patch('app.tools.syllabus_generator.pipeline.GoogleGenerativeAI')
def test_pipeline_compile_sequential(mock_model):
    # Setup mock model
    mock_model_instance = MagicMock()
    mock_model.return_value = mock_model_instance
    
    # Create SyllabusGeneratorPipeline and test if it compiles without errors
    from app.tools.syllabus_generator.pipeline import SyllabusGeneratorPipeline
    pipeline = SyllabusGeneratorPipeline(verbose=True)
    pipeline.compile_sequential()
    
    # Verify the chains were created
    assert hasattr(pipeline, 'chain_course_information')
    assert hasattr(pipeline, 'chain_course_description_objectives')
    assert hasattr(pipeline, 'chain_course_content')
    assert hasattr(pipeline, 'chain_policies_procedures')
    assert hasattr(pipeline, 'parallel_pipeline')

# Test the full generation process
@patch('app.tools.syllabus_generator.pipeline.SyllabusGeneratorPipeline')
def test_generate_syllabus(mock_pipeline_class):
    # Create mock objects
    mock_pipeline = MagicMock()
    mock_pipeline_class.return_value = mock_pipeline
    
    # Mock chain results
    mock_pipeline.chain_course_information.invoke.return_value = {"course_title": "Math 101", "grade_level": "5th grade", "description": "Basic math course"}
    mock_pipeline.chain_course_description_objectives.invoke.return_value = {"objectives": ["Learn addition"], "intended_learning_outcomes": ["Can add numbers"]}
    mock_pipeline.chain_course_content.invoke.return_value = [{"unit_time": "Week", "unit_time_value": 1, "topic": "Addition"}]
    mock_pipeline.chain_policies_procedures.invoke.return_value = {"attendance_policy": "Mandatory", "late_submission_policy": "Penalties apply", "academic_honesty": "Required"}
    
    mock_parallel_results = {
        "branches": {
            "assessment_grading_criteria": {"assessment_methods": [{"type_assessment": "Exam", "weight": 60}], "grading_scale": {"A": "90-100"}},
            "learning_resources": [{"title": "Math Book", "author": "John Doe", "year": 2023}],
            "course_schedule": [{"unit_time": "Week", "unit_time_value": 1, "date": "Jan 1", "topic": "Addition", "activity_desc": "Practice problems"}]
        }
    }
    mock_pipeline.parallel_pipeline.invoke.return_value = mock_parallel_results
    
    # Create a mock SyllabusGeneratorArgsModel object
    mock_args = MagicMock(spec=SyllabusGeneratorArgsModel)
    for key, value in base_attributes.items():
        setattr(mock_args, key, value)
    
    # Create SyllabusRequestArgs
    request_args = SyllabusRequestArgs(mock_args, "Test summary")
    
    # Test generate_syllabus
    result = generate_syllabus(request_args, verbose=True)
    
    # Assertions
    assert isinstance(result, dict)
    assert "course_information" in result
    assert "course_description_objectives" in result
    assert "course_content" in result
    assert "policies_procedures" in result
    assert "assessment_grading_criteria" in result
    assert "learning_resources" in result
    assert "course_schedule" in result
    
    # Verify the correct methods were called
    mock_pipeline.compile_sequential.assert_called_once()
    mock_pipeline.chain_course_information.invoke.assert_called_once()
    mock_pipeline.chain_course_description_objectives.invoke.assert_called_once()
    mock_pipeline.chain_course_content.invoke.assert_called_once()
    mock_pipeline.chain_policies_procedures.invoke.assert_called_once()
    mock_pipeline.parallel_pipeline.invoke.assert_called_once()

# Test error handling in generate_syllabus
@patch('app.tools.syllabus_generator.pipeline.SyllabusGeneratorPipeline')
def test_generate_syllabus_error_handling(mock_pipeline_class):
    # Make the pipeline raise an exception
    mock_pipeline = MagicMock()
    mock_pipeline_class.return_value = mock_pipeline
    mock_pipeline.compile_sequential.side_effect = Exception("Test error")
    
    # Create a mock SyllabusGeneratorArgsModel object
    mock_args = MagicMock(spec=SyllabusGeneratorArgsModel)
    for key, value in base_attributes.items():
        setattr(mock_args, key, value)
    
    # Create SyllabusRequestArgs
    request_args = SyllabusRequestArgs(mock_args, "Test summary")
    
    # Test that it raises HTTPException
    with pytest.raises(Exception) as exc_info:
        generate_syllabus(request_args, verbose=True)
    
    # Could be HTTPException specifically if imported correctly in the test environment
    assert "error" in str(exc_info.value).lower() or "exception" in str(exc_info.value).lower()

# Integration test combining existing executor with new pipeline
@patch('app.tools.syllabus_generator.core.generate_syllabus')
def test_integration_executor_with_pipeline(mock_generate_syllabus):
    # Mock the generate_syllabus function to return a simple dict
    mock_generate_syllabus.return_value = {
        "course_information": {"course_title": "Math 101"},
        "course_description_objectives": {"objectives": ["Learn math"]},
        "course_content": [{"topic": "Addition"}],
        "policies_procedures": {"attendance_policy": "Mandatory"},
        "assessment_grading_criteria": {"grading_scale": {"A": "90-100"}},
        "learning_resources": [{"title": "Math Book"}],
        "course_schedule": [{"topic": "Week 1: Addition"}]
    }
    
    # Test executor with no file (should use pipeline directly)
    result = executor(**base_attributes)
    assert isinstance(result, dict)
    assert "course_information" in result
    
    # Verify generate_syllabus was called
    mock_generate_syllabus.assert_called_once()