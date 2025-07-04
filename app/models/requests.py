from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class AnalysisType(str, Enum):
    SENTIMENT = "sentiment"
    SUMMARY = "summary"
    COMPREHENSIVE = "comprehensive"

class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    analysis_type: AnalysisType = AnalysisType.COMPREHENSIVE

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    context: Optional[str] = Field(None, max_length=5000)
    conversation_id: Optional[str] = None