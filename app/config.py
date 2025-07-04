from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    MAX_FILE_SIZE: int = 10485760
    UPLOAD_DIR: str = "./uploads"
    
    class Config:
        env_file = ".env"

settings = Settings()