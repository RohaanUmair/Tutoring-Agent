# src/api/routes/agent_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
import sys
import os

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, src_dir)
sys.path.insert(0, os.path.join(src_dir, 'math_tutoring_agent'))

from math_tutoring_agent.orchestrator_agent import main_math_agent
from math_tutoring_agent.Config.config import config
from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent

# Add the utils path
sys.path.insert(0, os.path.join(src_dir))
from utils.voice_utils import format_for_speech

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    text: str
    speech_text: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Send message to math agent and get response
    """
    try:
        # Collect the full response from streaming
        full_response = ""
        
        agent_response = Runner.run_streamed(
            main_math_agent,
            input=request.message,
            run_config=config
        )
        
        async for event in agent_response.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                full_response += event.data.delta
        
        # Format for speech
        speech_response = format_for_speech(full_response)
        
        return ChatResponse(
            text=full_response,
            speech_text=speech_response
        )
    
    except Exception as e:
        print(f"Error in chat: {str(e)}")  # Debug
        import traceback
        traceback.print_exc()  # Print full error
        
        return ChatResponse(
            text=f"Sorry, I encountered an error: {str(e)}",
            speech_text="Sorry, I encountered an error"
        )