from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.image_service import ImageService
from app.models.responses import ImageAnalysisResponse
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze uploaded image using Google Gemini Vision
    
    - **file**: Image file (JPEG, PNG, WebP, max 10MB)
    
    Returns detailed analysis including:
    - Object detection and description
    - Color analysis
    - Text detection (OCR)
    - Mood and composition analysis
    - Technical suggestions
    """
    try:
        logger.info(f"Analyzing image: {file.filename}")
        image_service = ImageService()
        return await image_service.analyze_uploaded_image(file)
        
    except Exception as e:
        logger.error(f"Image analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))