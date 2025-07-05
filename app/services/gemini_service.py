import google.generativeai as genai
import json
from typing import Dict, Any
from app.core.config import settings
from app.core.exceptions import AIServiceException
from app.core.logging import get_logger

logger = get_logger(__name__)

class GeminiService:
    def __init__(self):
        """Initialize Gemini service"""
        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.text_model = genai.GenerativeModel('gemini-1.5-flash')
            self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini service: {e}")
            raise AIServiceException("Failed to initialize AI service")
    
    async def test_connection(self) -> bool:
        """Test Gemini API connection"""
        try:
            response = self.text_model.generate_content("Test connection")
            return True
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False
    
    async def analyze_image_with_vision(self, image_data: bytes, content_type: str) -> Dict[str, Any]:
        """Analyze image using Gemini Vision"""
        try:
            image_part = {
                "mime_type": content_type,
                "data": image_data
            }
            
            prompt = """
            Analyze this image comprehensively and provide a detailed JSON response:
            {
                "description": "Detailed description of what you see in the image",
                "objects": ["list", "of", "detected", "objects"],
                "colors": ["dominant", "colors", "present"],
                "text_detected": "any visible text in the image",
                "mood": "overall mood or atmosphere",
                "composition": "description of visual composition",
                "suggestions": "insights or potential improvements",
                "confidence": 0.95
            }
            
            Ensure the response is valid JSON format.
            """
            
            response = self.vision_model.generate_content([prompt, image_part])
            return self._parse_json_response(response.text)
            
        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            # Return a structured error response
            return {
                "description": f"Analysis failed: {str(e)}",
                "objects": [],
                "colors": [],
                "text_detected": "",
                "mood": "unknown",
                "composition": "",
                "suggestions": "Please try again",
                "confidence": 0.0,
                "error": str(e)
            }
    
    async def analyze_text_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment"""
        try:
            prompt = f"""
            Analyze the sentiment and characteristics of this text:
            
            Text: "{text}"
            
            Provide a JSON response with:
            {{
                "overall_sentiment": "positive/negative/neutral",
                "confidence_score": 0.85,
                "emotions": ["joy", "excitement", "concern"],
                "key_phrases": ["important phrases from the text"],
                "tone": "formal/informal/conversational/etc",
                "subjectivity": "objective/subjective",
                "intensity": "low/medium/high"
            }}
            """
            
            response = self.text_model.generate_content(prompt)
            return self._parse_json_response(response.text)
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            raise AIServiceException(f"Sentiment analysis failed: {str(e)}")
    
    async def summarize_text(self, text: str) -> Dict[str, Any]:
        """Summarize text content"""
        try:
            prompt = f"""
            Summarize this text and provide analysis:
            
            Text: "{text}"
            
            Provide a JSON response with:
            {{
                "summary": "Concise summary of the main points",
                "key_points": ["main", "points", "extracted"],
                "themes": ["central", "themes", "identified"],
                "word_count_original": {len(text.split())},
                "reading_time_minutes": 2,
                "complexity": "simple/moderate/complex"
            }}
            """
            
            response = self.text_model.generate_content(prompt)
            return self._parse_json_response(response.text)
            
        except Exception as e:
            logger.error(f"Text summarization failed: {e}")
            raise AIServiceException(f"Text summarization failed: {str(e)}")
    
    async def comprehensive_text_analysis(self, text: str) -> Dict[str, Any]:
        """Comprehensive text analysis"""
        try:
            prompt = f"""
            Provide a comprehensive analysis of this text:
            
            Text: "{text}"
            
            Analyze and provide JSON response with:
            {{
                "sentiment": {{
                    "overall": "positive/negative/neutral",
                    "confidence": 0.85,
                    "emotions": ["detected", "emotions"]
                }},
                "summary": "Brief but comprehensive summary",
                "key_topics": ["main", "topics", "discussed"],
                "writing_style": "Description of writing style and approach",
                "readability": "easy/moderate/difficult",
                "target_audience": "Who this seems written for",
                "intent": "What the author seems to want to achieve",
                "entities": ["people", "places", "organizations", "mentioned"],
                "suggestions": "Potential improvements or insights"
            }}
            """
            
            response = self.text_model.generate_content(prompt)
            return self._parse_json_response(response.text)
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            raise AIServiceException(f"Text analysis failed: {str(e)}")
    
    async def chat_response(self, message: str, context: str = "") -> str:
        """Generate chat response"""
        try:
            context_prompt = f"Context: {context}\n\n" if context else ""
            
            prompt = f"""
            {context_prompt}User message: {message}
            
            Please provide a helpful, conversational response. If there's context about previously analyzed content, refer to it naturally in your response. Be engaging and informative.
            """
            
            response = self.text_model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Chat response failed: {e}")
            raise AIServiceException(f"Chat response failed: {str(e)}")
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON from Gemini response"""
        try:
            # Find JSON in response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                # No JSON found, return structured response
                return {
                    "raw_response": response_text,
                    "parsed": False,
                    "error": "No JSON structure found in response"
                }
            
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON from Gemini response")
            return {
                "raw_response": response_text,
                "parsed": False,
                "error": "Invalid JSON format"
            }
