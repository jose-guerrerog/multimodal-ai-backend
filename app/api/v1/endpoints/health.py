from fastapi import APIRouter
from app.models.responses import HealthResponse
from app.services.gemini_service import GeminiService
from app.core.config import settings
from app.utils.time_utils import get_current_timestamp

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    gemini_service = GeminiService()
    
    # Test Gemini connection
    gemini_status = "connected" if await gemini_service.test_connection() else "disconnected"
    
    return HealthResponse(
        status="healthy" if gemini_status == "connected" else "unhealthy",
        gemini_api=gemini_status,
        timestamp=get_current_timestamp(),
        version=settings.VERSION
    )

@router.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": f"{settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "health_check": "/api/v1/health",
        "endpoints": {
            "image_analysis": "/api/v1/images/analyze",
            "text_analysis": "/api/v1/text/analyze",
            "chat": "/api/v1/chat/message",
            "conversations": "/api/v1/chat/conversations"
        }
    }
