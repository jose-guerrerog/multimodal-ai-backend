from fastapi import UploadFile
from app.services.gemini_service import GeminiService
from app.models.responses import ImageAnalysisResponse
from app.core.logging import get_logger
import time
import json

logger = get_logger(__name__)

class ImageService:
    def __init__(self):
        self.gemini_service = GeminiService()
    
    async def analyze_uploaded_image(self, file: UploadFile) -> ImageAnalysisResponse:
        """Process and analyze uploaded image (no file saving)"""
        start_time = time.time()
        
        try:
            # Validate file type
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
            if file.content_type not in allowed_types:
                raise Exception("Invalid file type. Please upload JPEG, PNG, or WebP images.")
            
            # Validate file size (10MB max)
            max_size = 10 * 1024 * 1024
            if file.size and file.size > max_size:
                raise Exception("File too large. Maximum size is 10MB.")
            
            # Read file content directly (no saving to disk)
            await file.seek(0)
            image_data = await file.read()
            
            # Analyze with Gemini Vision
            analysis_result = await self.gemini_service.analyze_image_with_vision(
                image_data, file.content_type
            )
            
            processing_time = f"{time.time() - start_time:.2f}s"
            
            return ImageAnalysisResponse(
                success=True,
                filename=file.filename or "unknown.jpg",
                analysis=analysis_result,
                processing_time=processing_time,
                file_size=file.size
            )
            
        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            processing_time = f"{time.time() - start_time:.2f}s"
            
            return ImageAnalysisResponse(
                success=False,
                filename=file.filename or "unknown.jpg",
                analysis={"error": str(e)},
                processing_time=processing_time,
                file_size=file.size
            )