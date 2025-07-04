from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import FileValidationException

def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file"""
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise FileValidationException(
            f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
        )
    
    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise FileValidationException(
            f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
        )

def validate_text_length(text: str, max_length: int = 10000) -> None:
    """Validate text length"""
    if len(text.strip()) == 0:
        raise FileValidationException("Text cannot be empty")
    
    if len(text) > max_length:
        raise FileValidationException(f"Text too long. Maximum length: {max_length} characters")
