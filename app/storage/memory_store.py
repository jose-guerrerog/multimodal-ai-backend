from typing import Dict, Optional, List
from app.models.chat import ChatMessage, Conversation, ConversationSummary
from app.utils.time_utils import get_current_timestamp
from app.core.logging import get_logger

logger = get_logger(__name__)

class ConversationStore:
    """In-memory storage for conversations (use Redis/DB in production)"""
    
    def __init__(self):
        self._conversations: Dict[str, Conversation] = {}
    
    def create_conversation(self, conversation_id: str) -> Conversation:
        """Create a new conversation"""
        timestamp = get_current_timestamp()
        conversation = Conversation(
            conversation_id=conversation_id,
            messages=[],
            created_at=timestamp,
            last_activity=timestamp
        )
        self._conversations[conversation_id] = conversation
        logger.info(f"Created new conversation: {conversation_id}")
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        return self._conversations.get(conversation_id)
    
    def add_message(self, conversation_id: str, message: ChatMessage) -> None:
        """Add message to conversation"""
        if conversation_id not in self._conversations:
            self.create_conversation(conversation_id)
        
        conversation = self._conversations[conversation_id]
        conversation.messages.append(message)
        conversation.last_activity = get_current_timestamp()
        
        logger.info(f"Added message to conversation {conversation_id}")
    
    def list_conversations(self) -> List[ConversationSummary]:
        """List all conversations with summaries"""
        summaries = []
        for conv_id, conversation in self._conversations.items():
            preview = ""
            if conversation.messages:
                first_message = conversation.messages[0].user
                preview = first_message[:50] + "..." if len(first_message) > 50 else first_message
            
            summary = ConversationSummary(
                conversation_id=conv_id,
                message_count=len(conversation.messages),
                created_at=conversation.created_at,
                last_activity=conversation.last_activity,
                preview=preview
            )
            summaries.append(summary)
        
        # Sort by last activity (most recent first)
        summaries.sort(key=lambda x: x.last_activity, reverse=True)
        return summaries
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete conversation"""
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            logger.info(f"Deleted conversation: {conversation_id}")
            return True
        return False
    
    def get_stats(self) -> Dict[str, int]:
        """Get storage statistics"""
        total_conversations = len(self._conversations)
        total_messages = sum(len(conv.messages) for conv in self._conversations.values())
        
        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "active_conversations": total_conversations  # All are active in memory
        }