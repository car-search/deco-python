import json

from opentelemetry.semconv._incubating.attributes import gen_ai_attributes as GenAIAttributes
from src.amint.semconv import amint_gen_ai_attributes as AmintGenAIAttributes


def process_response(span, response):
    if not response:
        return

    raw_attributes = {
        **_parse_response_metadata(response),
        **_parse_response_usage(response),
        **_parse_response_reasoning(response),
        **_parse_response_output(response),
    }

    attributes = {k: v for k, v in raw_attributes.items() if v is not None}
    span.set_attributes(attributes)

def _parse_response_metadata(response):
    return {
        GenAIAttributes.GEN_AI_RESPONSE_ID: response.get("id"),
        GenAIAttributes.GEN_AI_RESPONSE_MODEL: response.get("model"),
        AmintGenAIAttributes.GEN_AI_RESPONSE_SERVICE_TIER: response.get("service_tier"),
    }

def _parse_response_usage(response):
    usage = response.get("usage")
    if not usage:
        return {}

    attributes = {
        AmintGenAIAttributes.GEN_AI_USAGE_TOTAL_TOKENS: usage.get("total_tokens"),
    }

    # Input details
    input_details = usage.get("input_tokens_details")
    if input_details:
        input_tokens_total = usage.get("input_tokens")
        input_tokens_cached = input_details.get("cached_tokens")
        input_tokens_input = input_tokens_total - input_tokens_cached

        attributes.update({
            AmintGenAIAttributes.GEN_AI_USAGE_INPUT_TOKENS_TOTAL: input_tokens_total,
            AmintGenAIAttributes.GEN_AI_USAGE_INPUT_TOKENS_INPUT: input_tokens_input,
            AmintGenAIAttributes.GEN_AI_USAGE_INPUT_TOKENS_CACHED: input_tokens_cached,
        })

    # Output details
    output_details = usage.get("output_tokens_details")
    if output_details:
        output_tokens_total = usage.get("output_tokens")
        output_tokens_reasoning = output_details.get("reasoning_tokens")
        output_tokens_output = output_tokens_total - output_tokens_reasoning

        attributes.update({
            AmintGenAIAttributes.GEN_AI_USAGE_OUTPUT_TOKENS_TOTAL: output_tokens_total,
            AmintGenAIAttributes.GEN_AI_USAGE_OUTPUT_TOKENS_OUTPUT: output_tokens_output,
            AmintGenAIAttributes.GEN_AI_USAGE_OUTPUT_TOKENS_REASONING: output_tokens_reasoning,
        })
    return attributes

def _parse_response_reasoning(response):
    reasoning = response.get("reasoning")
    if not reasoning:
        return {}

    return {
        AmintGenAIAttributes.GEN_AI_RESPONSE_REASONING_EFFORT: reasoning.get("effort"),
        AmintGenAIAttributes.GEN_AI_RESPONSE_REASONING_SUMMARY: reasoning.get("summary"),
    }

def _parse_response_output(response):
    output_messages = response.get("output")
    if not output_messages:
        return {}

    return {
        GenAIAttributes.GEN_AI_OUTPUT_MESSAGES: json.dumps(output_messages),
        GenAIAttributes.GEN_AI_OUTPUT_TYPE: GenAIAttributes.GenAiOutputTypeValues.TEXT.value,
    }