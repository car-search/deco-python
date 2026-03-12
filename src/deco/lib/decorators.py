import functools
import logging
from typing import Callable, TypeVar, ParamSpec

# Create a logger specific to your SDK
logger = logging.getLogger("my_sdk")

P = ParamSpec("P")
R = TypeVar("R")

def _create_decorator() -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Using the logger instead of print
            logger.info("Executing function: %s", func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return decorator

workflow = _create_decorator()