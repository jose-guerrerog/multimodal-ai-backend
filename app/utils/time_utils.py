from datetime import datetime
import time
from typing import Any, Callable

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat() + "Z"

def time_function(func: Callable) -> Callable:
    """Decorator to time function execution"""
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, f"{execution_time:.2f}s"
    return wrapper

async def async_time_function(func: Callable) -> Callable:
    """Decorator to time async function execution"""
    async def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, f"{execution_time:.2f}s"
    return wrapper