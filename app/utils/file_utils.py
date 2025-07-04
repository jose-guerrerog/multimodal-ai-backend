import aiofiles
import uuid
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings

async def save_upload_file(file: UploadFile) -> str:
    """Save uploaded file and return file path"""
    file_id = str(uuid.uuid4())
    file_extension = file.filename.split(".")[-1] if file.filename else "jpg"
    file_path = Path(settings.UPLOAD_DIR) / f"{file_id}.{file_extension}"
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return str(file_path)

def cleanup_file(file_path: str) -> None:
    """Remove temporary file"""
    try:
        Path(file_path).unlink(missing_ok=True)
    except Exception:
        pass  # Log error in production