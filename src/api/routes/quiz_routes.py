# src/api/routes/quiz_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
import sys
import os

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, src_dir)
sys.path.insert(0, os.path.join(src_dir, 'quiz_agent'))

from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent

router = APIRouter()

class QuizRequest(BaseModel):
    class_subject: str  # Example: "class 9 math", "10 physics"
    topic: str = "target paper 2025"

class QuizResponse(BaseModel):
    text: str

@router.post("/generate-paper", response_model=QuizResponse)
async def generate_quiz_paper(request: QuizRequest):
    """
    Generate quiz paper using master_quiz_agent
    """
    try:
        # Import and initialize the master quiz agent
        from quiz_agent.master_quiz_agent import agent_mapping
        
        # Find the right agent based on class and subject
        selected_agent = None
        user_input_lower = request.class_subject.lower()
        
        for key, agent in agent_mapping.items():
            if key in user_input_lower:
                selected_agent = agent
                break
        
        if not selected_agent:
            return QuizResponse(
                text="❌ Please specify class and subject clearly.\nAvailable: Class 9/10 - Math, Physics, Chemistry, Biology, Computer, English"
            )
        
        # Collect the full response from streaming
        full_response = f"🔍 Generating paper for: {request.class_subject.upper()}\n\n"
        
        agent_response = Runner.run_streamed(
            selected_agent,
            input=request.topic,
            run_config=agent_mapping['config']  # You'll need to handle config
        )
        
        async for event in agent_response.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                full_response += event.data.delta
        
        return QuizResponse(text=full_response)
    
    except Exception as e:
        print(f"Error generating quiz paper: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return QuizResponse(
            text=f"❌ Error generating paper: {str(e)}"
        )

@router.get("/available-subjects")
async def get_available_subjects():
    """
    Get list of available classes and subjects
    """
    try:
        from quiz_agent.master_quiz_agent import agent_mapping
        
        subjects = list(agent_mapping.keys())
        # Remove config if it exists
        if 'config' in subjects:
            subjects.remove('config')
            
        return {
            "available_subjects": subjects,
            "examples": [
                "class 9 math",
                "10 physics", 
                "biology class 9",
                "9 bio",
                "class 10 chemistry"
            ]
        }
    
    except Exception as e:
        return {"error": str(e)}