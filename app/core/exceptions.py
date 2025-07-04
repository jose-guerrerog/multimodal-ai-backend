from fastapi import HTTPException

class AIServiceException(HTTPException):
    def __init__(self, detail: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)

class FileValidationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class RateLimitException(HTTPException):
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(status_code=429, detail=detail)