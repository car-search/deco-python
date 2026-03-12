import json

from src.amint.semconv import amint_gen_ai_attributes as AmintGenAIAttributes
from opentelemetry.semconv._incubating.attributes import gen_ai_attributes as GenAIAttributes


def process_response(span, response):
    if not response:
        return

    raw_attributes = {
        **_parse_response_metadata(response),
        **_parse_response_usage(response),
        **_parse_response_output(response),
    }

    attributes = {k: v for k, v in raw_attributes.items() if v is not None}
    span.set_attributes(attributes)

def _parse_response_metadata(response):
    return {
        GenAIAttributes.GEN_AI_RESPONSE_ID: response.get("id"),
        GenAIAttributes.GEN_AI_RESPONSE_MODEL: response.get("model"),
        GenAIAttributes.GEN_AI_RESPONSE_FINISH_REASONS: response.get("stop_reason"),
    }

def _parse_response_usage(response):
    usage = response.get("usage")
    if not usage:
        return {}

    input_tokens_cache_read  = usage.get("cache_read_input_tokens")
    input_tokens_cache_creation  = usage.get("cache_creation_input_tokens")
    input_tokens_cached = input_tokens_cache_read + input_tokens_cache_creation
    input_tokens_input = usage.get("input_tokens")
    input_tokens_total = input_tokens_input + input_tokens_cached

    output_tokens_output = usage.get("output_tokens")
    output_tokens_total = output_tokens_output

    total_tokens = input_tokens_total + output_tokens_total

    return {
        AmintGenAIAttributes.GEN_AI_USAGE_INPUT_TOKENS_CACHE_READ: input_tokens_cache_read,
        AmintGenAIAttributes.GEN_AI_USAGE_INPUT_TOKENS_CACHE_CREATION: input_tokens_cache_creation,
        AmintGenAIAttributes.GEN_AI_USAGE_INPUT_TOKENS_CACHED: input_tokens_cached,
        AmintGenAIAttributes.GEN_AI_USAGE_INPUT_TOKENS_INPUT: input_tokens_input,
        AmintGenAIAttributes.GEN_AI_USAGE_INPUT_TOKENS_TOTAL: input_tokens_total,

        AmintGenAIAttributes.GEN_AI_USAGE_OUTPUT_TOKENS_OUTPUT: output_tokens_output,
        AmintGenAIAttributes.GEN_AI_USAGE_OUTPUT_TOKENS_TOTAL: output_tokens_total,

        AmintGenAIAttributes.GEN_AI_USAGE_TOTAL_TOKENS: total_tokens,

        AmintGenAIAttributes.GEN_AI_RESPONSE_SERVICE_TIER: usage.get("service_tier"),
    }

def _parse_response_output(response):
    output_messages = response.get("content")
    if not output_messages:
        return {}

    return {
        GenAIAttributes.GEN_AI_OUTPUT_MESSAGES: json.dumps(output_messages),
        GenAIAttributes.GEN_AI_OUTPUT_TYPE: GenAIAttributes.GenAiOutputTypeValues.TEXT.value,
    }