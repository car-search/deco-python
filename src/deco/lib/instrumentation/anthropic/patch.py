import json

from opentelemetry.semconv._incubating.attributes import gen_ai_attributes as GenAIAttributes

from .utils import process_response
from ...semconv import amint_gen_ai_attributes as AmintGenAIAttributes


def messages_create(tracer):
    def traced_method(wrapped, args, kwargs):

        span_name = f"anthropic.messages"

        output_config = kwargs.get("output_config", {})
        response_format = output_config.get("format", {})
        messages = kwargs.get("messages", {})

        raw_attributes = {
            # Operation & Provider
            GenAIAttributes.GEN_AI_OPERATION_NAME: GenAIAttributes.GenAiOperationNameValues.CHAT.value,
            GenAIAttributes.GEN_AI_PROVIDER_NAME: GenAIAttributes.GenAiProviderNameValues.ANTHROPIC.value,

            # Request
            GenAIAttributes.GEN_AI_REQUEST_MAX_TOKENS: kwargs.get("max_tokens"),
            GenAIAttributes.GEN_AI_REQUEST_MODEL: kwargs.get("model"),
            GenAIAttributes.GEN_AI_REQUEST_TEMPERATURE: kwargs.get("temperature"),
            GenAIAttributes.GEN_AI_REQUEST_TOP_P: kwargs.get("top_p"),
            GenAIAttributes.GEN_AI_REQUEST_STOP_SEQUENCES: kwargs.get("stop_sequences"),

            AmintGenAIAttributes.GEN_AI_REQUEST_INPUT: json.dumps(messages),
            AmintGenAIAttributes.GEN_AI_REQUEST_INSTRUCTIONS: kwargs.get("instructions"),
            AmintGenAIAttributes.GEN_AI_REQUEST_REASONING_EFFORT: output_config.get("effort"),
            AmintGenAIAttributes.GEN_AI_REQUEST_STORE: kwargs.get("store"),
            AmintGenAIAttributes.GEN_AI_REQUEST_RESPONSE_FORMAT: json.dumps(response_format),
            AmintGenAIAttributes.GEN_AI_REQUEST_SERVICE_TIER: kwargs.get("service_tier"),

        }

        attributes = {
            k: v for k, v in raw_attributes.items()
            if v is not None
        }

        with tracer.start_as_current_span(span_name, attributes=attributes) as span:
            response = wrapped(*args, **kwargs)
            process_response(
                span=span,
                response=response.model_dump()
            )
            return response

    return traced_method