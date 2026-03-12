import wrapt
import inspect

from typing import Optional, Callable
from .trace import telemetry


def _set_span_metadata(span, kind: str, name: str):
    span.set_attribute("acme.span.kind", kind)
    span.set_attribute("acme.span.name", name)


def _create_decorator(span_kind: str):
    def decorator(name: Optional[str] = None):

        def _get_wrapper(func: Callable):
            tracer = telemetry.tracer
            span_name = name if isinstance(name, str) else func.__name__

            @wrapt.decorator
            async def async_wrapper(wrapped, instance, args, kwargs):
                with tracer.start_as_current_span(span_name) as span:
                    _set_span_metadata(span, span_kind, span_name)
                    return await wrapped(*args, **kwargs)

            @wrapt.decorator
            def sync_wrapper(wrapped, instance, args, kwargs):
                with tracer.start_as_current_span(span_name) as span:
                    _set_span_metadata(span, span_kind, span_name)
                    return wrapped(*args, **kwargs)

            wrapper = async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper
            return wrapper(func)

        return _get_wrapper(name) if callable(name) else _get_wrapper

    return decorator


workflow = _create_decorator("workflow")
task = _create_decorator("task")
agent = _create_decorator("agent")
tool = _create_decorator("tool")