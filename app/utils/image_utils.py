from PIL import Image
import io
from typing import Tuple

def prepare_image_for_gemini(image_path: str) -> bytes:
    """Prepare image for Gemini Vision API"""
    with Image.open(image_path) as img:
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        max_size = (1024, 1024)
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=85)
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()

def get_image_info(image_path: str) -> dict:
    """Get basic image information"""
    with Image.open(image_path) as img:
        return {
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode,
            "size_mb": Path(image_path).stat().st_size / (1024 * 1024)
        }