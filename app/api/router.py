import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Union
from app.assistants.utils.assistants_utilities import execute_assistant
from app.services.schemas import GenericAssistantRequest, ToolRequest, ChatRequest, Message, ChatResponse, ToolResponse
from app.utils.auth import key_check
from app.services.logger import setup_logger
from app.api.error_utilities import InputValidationError, ErrorResponse
from app.tools.utils.tool_utilities import load_tool_metadata, execute_tool, finalize_inputs
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

logger = setup_logger(__name__)
router = APIRouter()

@router.get("/")
def read_root():
    from app.tools.multiple_choice_quiz_generator.core import executor
    
    import os
    
    import os
    
    file_url = "https://file.notion.so/f/f/e0e4952d-ee69-4824-9a41-54b460bb8b56/11f3af4e-09e3-4384-a310-1018d784bdfa/Science_Glossary.pdf?table=block&id=19745624-7e0a-81ac-b88b-dc64fb11ef75&spaceId=e0e4952d-ee69-4824-9a41-54b460bb8b56&expirationTimestamp=1740016800000&signature=2OerVCa9GAbhu-NPzbcSA8mJRfKt9FRtBQmIErDs35o&downloadName=Science_Glossary.pdf"
    
    quiz = executor(
        topic="Science Terms Vocabulary - 7th Grade Physics, Chemistry, and Biology",
        n_questions=10,
        file_url=file_url,
        file_type="pdf",
        lang="en"
    )
    return {"quiz": quiz}

@router.post("/submit-tool", response_model=Union[ToolResponse, ErrorResponse])
async def submit_tool( data: ToolRequest, _ = Depends(key_check)):     
    try: 
        # Unpack GenericRequest for tool data
        request_data = data.tool_data
        
        requested_tool = load_tool_metadata(request_data.tool_id)
        
        request_inputs_dict = finalize_inputs(request_data.inputs, requested_tool['inputs'])

        result = execute_tool(request_data.tool_id, request_inputs_dict)
        
        return ToolResponse(data=result)
    
    except InputValidationError as e:
        logger.error(f"InputValidationError: {e}")

        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(ErrorResponse(status=400, message=e.message))
        )
    
    except HTTPException as e:
        logger.error(f"HTTPException: {e}")
        return JSONResponse(
            status_code=e.status_code,
            content=jsonable_encoder(ErrorResponse(status=e.status_code, message=e.detail))
        )

@router.post("/assistant-chat", response_model=ChatResponse)
async def assistants( request: GenericAssistantRequest, _ = Depends(key_check) ):
    
    assistant_group = request.assistant_inputs.assistant_group
    assistant_name = request.assistant_inputs.assistant_name
    user_info = request.assistant_inputs.user_info
    messages = request.assistant_inputs.messages

    result = execute_assistant(assistant_group, assistant_name, user_info, messages)

    formatted_response = Message(
        role="ai",
        type="text",
        payload={"text": result}
    )
    
    return ChatResponse(data=[formatted_response])