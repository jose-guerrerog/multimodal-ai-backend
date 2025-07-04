from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime

class ImageAnalysisResponse(BaseModel):
    success: bool
    filename: str
    analysis: Dict[str, Any]
    processing_time: str
    file_size: Optional[int] = None

class TextAnalysisResponse(BaseModel):
    success: bool
    analysis_type: str
    analysis: Dict[str, Any]
    word_count: int
    character_count: int
    processing_time: str

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    gemini_api: str
    timestamp: str
    version: str

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: str