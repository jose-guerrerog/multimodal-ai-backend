from app.services.gemini_service import GeminiService
from app.storage.memory_store import ConversationStore
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse
from app.models.chat import ChatMessage, Conversation
from app.utils.time_utils import get_current_timestamp
from app.core.logging import get_logger
import uuid

logger = get_logger(__name__)

class ChatService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.conversation_store = ConversationStore()
    
    async def process_chat_message(self, request: ChatRequest) -> ChatResponse:
        """Process chat message and return AI response"""
        try:
            # Generate or use existing conversation ID
            conversation_id = request.conversation_id or str(uuid.uuid4())
            
            # Get conversation history for context
            conversation = self.conversation_store.get_conversation(conversation_id)
            
            # Build context for AI
            context = self._build_conversation_context(conversation, request.context)
            
            # Generate AI response
            ai_response = await self.gemini_service.chat_response(
                message=request.message,
                context=context
            )
            
            # Create message objects
            timestamp = get_current_timestamp()
            chat_message = ChatMessage(
                user=request.message,
                ai=ai_response,
                timestamp=timestamp
            )
            
            # Store in conversation
            self.conversation_store.add_message(conversation_id, chat_message)
            
            return ChatResponse(
                response=ai_response,
                conversation_id=conversation_id,
                timestamp=timestamp
            )
            
        except Exception as e:
            logger.error(f"Chat processing failed: {e}")
            raise
    
    def get_conversation_history(self, conversation_id: str) -> Conversation:
        """Get full conversation history"""
        return self.conversation_store.get_conversation(conversation_id)
    
    def _build_conversation_context(self, conversation: Conversation, additional_context: str = "") -> str:
        """Build context string for AI from conversation history"""
        context_parts = []
        
        # Add additional context if provided
        if additional_context:
            context_parts.append(f"Additional context: {additional_context}")
        
        # Add recent conversation history (last 5 messages)
        if conversation and conversation.messages:
            context_parts.append("Recent conversation:")
            for message in conversation.messages[-5:]:
                context_parts.append(f"User: {message.user}")
                context_parts.append(f"AI: {message.ai}")
        
        return "\n".join(context_parts)
