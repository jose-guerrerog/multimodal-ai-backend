from pydantic import BaseModel
from typing import List
from datetime import datetime

class ChatMessage(BaseModel):
    user: str
    ai: str
    timestamp: str

class Conversation(BaseModel):
    conversation_id: str
    messages: List[ChatMessage]
    created_at: str
    last_activity: str

class ConversationSummary(BaseModel):
    conversation_id: str
    message_count: int
    created_at: str
    last_activity: str
    preview: str  # First few words of conversation