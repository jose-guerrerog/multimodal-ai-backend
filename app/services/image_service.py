from fastapi import UploadFile
from app.services.gemini_service import GeminiService
from app.utils.file_utils import save_upload_file, cleanup_file
from app.utils.image_utils import prepare_image_for_gemini, get_image_info
from app.utils.validators import validate_image_file
from app.models.responses import ImageAnalysisResponse
from app.core.logging import get_logger
import time

logger = get_logger(__name__)

class ImageService:
    def __init__(self):
        self.gemini_service = GeminiService()
    
    async def analyze_uploaded_image(self, file: UploadFile) -> ImageAnalysisResponse:
        """Process and analyze uploaded image"""
        start_time = time.time()
        file_path = None
        
        try:
            # Validate file
            validate_image_file(file)
            
            # Save file temporarily
            file_path = await save_upload_file(file)
            
            # Get image info
            image_info = get_image_info(file_path)
            
            # Prepare for Gemini
            image_data = prepare_image_for_gemini(file_path)
            
            # Analyze with Gemini
            analysis_result = await self.gemini_service.analyze_image_with_vision(
                image_data, file.content_type
            )
            
            # Add image info to analysis
            analysis_result["image_info"] = image_info
            
            processing_time = f"{time.time() - start_time:.2f}s"
            
            return ImageAnalysisResponse(
                success=True,
                filename=file.filename or "unknown.jpg",
                analysis=analysis_result,
                processing_time=processing_time,
                file_size=file.size
            )
            
        finally:
            # Always cleanup temporary file
            if file_path:
                cleanup_file(file_path)