from fastapi import APIRouter, HTTPException
from typing import List
from app.services.chat_service import ChatService
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse
from app.models.chat import Conversation, ConversationSummary
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    Send a message to the AI chat system
    
    - **message**: Your message to the AI (max 1,000 characters)
    - **context**: Optional context about previously analyzed content
    - **conversation_id**: Optional conversation ID to continue existing chat
    
    Returns AI response with conversation tracking
    """
    try:
        logger.info(f"Processing chat message for conversation: {request.conversation_id}")
        chat_service = ChatService()
        return await chat_service.process_chat_message(request)
        
    except Exception as e:
        logger.error(f"Chat processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations", response_model=List[ConversationSummary])
async def list_conversations():
    """
    Get list of all conversations with summaries
    
    Returns list of conversation summaries ordered by most recent activity
    """
    try:
        chat_service = ChatService()
        return chat_service.conversation_store.list_conversations()
        
    except Exception as e:
        logger.error(f"Failed to list conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """
    Get full conversation history by ID
    
    - **conversation_id**: The conversation identifier
    
    Returns complete conversation with all messages
    """
    try:
        chat_service = ChatService()
        conversation = chat_service.get_conversation_history(conversation_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return conversation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete a conversation and all its messages
    
    - **conversation_id**: The conversation identifier to delete
    
    Returns success confirmation
    """
    try:
        chat_service = ChatService()
        deleted = chat_service.conversation_store.delete_conversation(conversation_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {"message": "Conversation deleted successfully", "conversation_id": conversation_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_chat_stats():
    """
    Get chat system statistics
    
    Returns statistics about conversations and messages
    """
    try:
        chat_service = ChatService()
        return chat_service.conversation_store.get_stats()
        
    except Exception as e:
        logger.error(f"Failed to get chat stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))