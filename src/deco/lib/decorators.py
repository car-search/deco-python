import logging
import functools
from typing import Any, TypeVar, Callable

# Create a logger specific to your SDK
logger = logging.getLogger("my_sdk")

R = TypeVar("R")

def _create_decorator() -> Callable[[Callable[..., R]], Callable[..., R]]:
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            # Using the logger instead of print
            logger.info("Executing function: %s", func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return decorator

workflow = _create_decorator()