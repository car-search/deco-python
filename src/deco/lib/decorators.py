import logging
import functools
from typing import Any, TypeVar, Callable

# Create a logger specific to your SDK
logger = logging.getLogger("my_sdk")

R = TypeVar("R")

def workflow(func: Callable[..., R]) -> Callable[..., R]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> R:
        logger.info("Executing function: %s", func.__name__)
        return func(*args, **kwargs)
    return wrapper