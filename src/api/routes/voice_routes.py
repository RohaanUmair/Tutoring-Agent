# src/api/routes/voice_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, src_dir)

from utils.voice_utils import get_voice_config

router = APIRouter()

class VoiceConfig(BaseModel):
    language: str
    rate: float
    pitch: float
    volume: float

@router.get("/config", response_model=VoiceConfig)
async def get_config():
    """Get voice configuration"""
    config = get_voice_config()
    return VoiceConfig(**config)