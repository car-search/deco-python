import atexit

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from .instrumentation.openai.instrumentor import OpenAIInstrumentor
from .instrumentation.anthropic.instrumentor import AnthropicInstrumentor


def get_resource():
    resource_attributes = {"service.name": "acme"}
    resource = Resource.create(resource_attributes)
    return resource


def get_processor():
    api_endpoint = "http://127.0.0.1:4317/v1/traces"
    exporter = OTLPSpanExporter(endpoint=api_endpoint)
    return SimpleSpanProcessor(exporter)


def init_tracer_provider():
    resource = get_resource()
    processor = get_processor()

    provider = TracerProvider(resource=resource)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    return provider


def init_instrumentations():
    instrumentors = [
        OpenAIInstrumentor(),
        AnthropicInstrumentor(),
    ]

    for instrumentor in instrumentors:
        try:
            instrumentor.instrument()

        except ModuleNotFoundError:
            pass

        except ImportError:
            pass


class TracerWrapper:
    _instance = None
    _provider = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._provider = init_tracer_provider()
            init_instrumentations()

            atexit.register(cls._instance.shutdown)
            print("Telemetry system online.")

        return cls._instance

    @property
    def tracer(self):
        return trace.get_tracer(__name__)

    def flush(self):
        if self._provider:
            self._provider.force_flush()

    def shutdown(self):
        if self._provider:
            self._provider.shutdown()
            self._provider = None


telemetry = TracerWrapper()
tracer = telemetry.tracer