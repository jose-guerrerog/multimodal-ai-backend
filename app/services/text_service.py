from app.services.gemini_service import GeminiService
from app.models.requests import TextAnalysisRequest, AnalysisType
from app.models.responses import TextAnalysisResponse
from app.utils.validators import validate_text_length
from app.core.logging import get_logger
import time

logger = get_logger(__name__)

class TextService:
    def __init__(self):
        self.gemini_service = GeminiService()
    
    async def analyze_text(self, request: TextAnalysisRequest) -> TextAnalysisResponse:
        """Analyze text based on analysis type"""
        start_time = time.time()
        
        # Validate input
        validate_text_length(request.text)
        
        # Perform analysis based on type
        if request.analysis_type == AnalysisType.SENTIMENT:
            analysis_result = await self.gemini_service.analyze_text_sentiment(request.text)
        elif request.analysis_type == AnalysisType.SUMMARY:
            analysis_result = await self.gemini_service.summarize_text(request.text)
        else:  # COMPREHENSIVE
            analysis_result = await self.gemini_service.comprehensive_text_analysis(request.text)
        
        processing_time = f"{time.time() - start_time:.2f}s"
        
        return TextAnalysisResponse(
            success=True,
            analysis_type=request.analysis_type.value,
            analysis=analysis_result,
            word_count=len(request.text.split()),
            character_count=len(request.text),
            processing_time=processing_time
        )