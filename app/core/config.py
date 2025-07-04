from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "AI Vision & Chat Hub"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Google Gemini
    GOOGLE_API_KEY: str
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Rate Limiting
    REQUESTS_PER_MINUTE: int = 15
    REQUESTS_PER_DAY: int = 1500
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()