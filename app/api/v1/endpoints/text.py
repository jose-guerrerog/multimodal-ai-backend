from fastapi import APIRouter, HTTPException
from app.services.text_service import TextService
from app.models.requests import TextAnalysisRequest
from app.models.responses import TextAnalysisResponse
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text using Google Gemini
    
    - **text**: Text content to analyze (max 10,000 characters)
    - **analysis_type**: Type of analysis (sentiment, summary, comprehensive)
    
    Returns detailed analysis based on the selected type:
    - **Sentiment**: Emotion analysis, tone, subjectivity
    - **Summary**: Key points, themes, reading time
    - **Comprehensive**: Full analysis including all aspects
    """
    try:
        logger.info(f"Analyzing text: {request.analysis_type} analysis")
        text_service = TextService()
        return await text_service.analyze_text(request)
        
    except Exception as e:
        logger.error(f"Text analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))