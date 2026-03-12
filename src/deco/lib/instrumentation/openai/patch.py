from opentelemetry.semconv._incubating.attributes import gen_ai_attributes as GenAIAttributes
from src.amint.semconv import amint_gen_ai_attributes as AmintGenAIAttributes
from .utils import process_response

import json

def responses_create(tracer):
    def traced_method(wrapped, instance, args, kwargs):

        span_name = f"openai.responses"

        reasoning = kwargs.get("reasoning", {})
        text = kwargs.get("text", {})
        input = kwargs.get("input", {})

        raw_attributes = {
            # Operation & Provider
            GenAIAttributes.GEN_AI_OPERATION_NAME: GenAIAttributes.GenAiOperationNameValues.CHAT.value,
            GenAIAttributes.GEN_AI_PROVIDER_NAME: GenAIAttributes.GenAiProviderNameValues.OPENAI.value,

            # Request
            GenAIAttributes.GEN_AI_REQUEST_MAX_TOKENS: kwargs.get("max_tokens"),
            GenAIAttributes.GEN_AI_REQUEST_MODEL: kwargs.get("model"),
            GenAIAttributes.GEN_AI_REQUEST_TEMPERATURE: kwargs.get("temperature"),
            GenAIAttributes.GEN_AI_REQUEST_TOP_P: kwargs.get("top_p"),
            GenAIAttributes.GEN_AI_REQUEST_STOP_SEQUENCES: kwargs.get("stop_sequences"),

            AmintGenAIAttributes.GEN_AI_REQUEST_INPUT: json.dumps(input),
            AmintGenAIAttributes.GEN_AI_REQUEST_INSTRUCTIONS: kwargs.get("instructions"),
            AmintGenAIAttributes.GEN_AI_REQUEST_REASONING_EFFORT: reasoning.get("effort"),
            AmintGenAIAttributes.GEN_AI_REQUEST_REASONING_SUMMARY: reasoning.get("summary"),
            AmintGenAIAttributes.GEN_AI_REQUEST_STORE: kwargs.get("store"),
            AmintGenAIAttributes.GEN_AI_REQUEST_RESPONSE_FORMAT: text.get("format"),
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