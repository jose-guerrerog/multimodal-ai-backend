from fastapi import APIRouter
from app.api.v1.endpoints import health, images, text, chat

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(text.router, prefix="/text", tags=["text"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
