from typing import Collection

from wrapt import wrap_function_wrapper
from opentelemetry.trace import get_tracer
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor

from .patch import *

_instruments = ("openai >= 0.27.0",)


# opentelemetry-python-contrib/opentelemetry-instrumentation/src/opentelemetry/instrumentation/instrumentation.py
class OpenAIInstrumentor(BaseInstrumentor):
    def __init__(self):
        super().__init__()
        self._tracer = None
        self._logger = None
        self._meter = None

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, tracer_provider)

        wrap_function_wrapper(
            "openai.resources.responses",
            "Responses.create",
            responses_create(tracer),
        )

    def _uninstrument(self):
        unwrap("openai.responses.create", "Responses.create")