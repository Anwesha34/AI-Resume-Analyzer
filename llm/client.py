import os
import json
from copy import deepcopy
from functools import lru_cache

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

MAX_PROMPT_TOKENS = 1800


@lru_cache(maxsize=1)
def get_llm():
    return ChatGroq(
        api_key=os.environ["GROQ_API_KEY"],
        model_name="llama-3.1-8b-instant",
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}},
    )


def _validate_schema(schema, payload):
    if hasattr(schema, "model_validate"):
        return schema.model_validate(payload)

    return schema.parse_obj(payload)


def _parse_json_object(text):
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model response.")

    return json.loads(text[start:end + 1])


def estimate_tokens(value):
    return max(1, len(str(value)) // 4)


def _trim_text(text, max_chars):
    text = str(text or "")
    return text if len(text) <= max_chars else text[:max_chars].rsplit(" ", 1)[0]


def _trim_list(items, max_items=8, max_chars=600):
    trimmed = []

    for item in list(items or [])[:max_items]:
        if isinstance(item, dict):
            trimmed.append(_trim_mapping(item, max_chars=max_chars))
        else:
            trimmed.append(_trim_text(item, max_chars))

    return trimmed


def _trim_mapping(mapping, max_chars=600):
    return {
        key: _trim_value(value, max_chars=max_chars)
        for key, value in dict(mapping or {}).items()
    }


def _trim_value(value, max_chars=600):
    if isinstance(value, str):
        return _trim_text(value, max_chars)
    if isinstance(value, list):
        return _trim_list(value, max_items=8, max_chars=max_chars)
    if isinstance(value, dict):
        return _trim_mapping(value, max_chars=max_chars)
    return value


def enforce_token_budget(values, max_tokens=MAX_PROMPT_TOKENS):
    compact_values = deepcopy(values)

    for max_items, max_chars in [(8, 600), (6, 400), (4, 280), (3, 200)]:
        estimated = estimate_tokens(compact_values)
        if estimated <= max_tokens:
            return compact_values

        compact_values = {
            key: (
                _trim_list(value, max_items=max_items, max_chars=max_chars)
                if isinstance(value, list)
                else _trim_mapping(value, max_chars=max_chars)
                if isinstance(value, dict)
                else _trim_text(value, max_chars * 2)
                if isinstance(value, str)
                else value
            )
            for key, value in compact_values.items()
        }

    return compact_values


def invoke_structured(schema, template, fallback=None, **values):
    parser = PydanticOutputParser(pydantic_object=schema)
    strict_template = """
Return ONLY one valid JSON object.
Do not include markdown, code fences, Python code, explanations, or prose.
The JSON object must match the schema exactly.

{template}
"""
    safe_values = enforce_token_budget(values)
    prompt = PromptTemplate(
        input_variables=list(safe_values),
        partial_variables={"format_instructions": parser.get_format_instructions()},
        template=strict_template.format(template=template),
    )
    try:
        response = get_llm().invoke(prompt.format(**safe_values))
    except Exception:
        if fallback is not None:
            return fallback
        raise

    try:
        return parser.parse(response.content)
    except Exception:
        try:
            return _validate_schema(schema, _parse_json_object(response.content))
        except Exception:
            if fallback is not None:
                return fallback
            raise


def build_compact_prompt(template, **values):
    safe_values = enforce_token_budget(values)
    return template.format(**safe_values)


def safe_llm_call(schema, template, fallback=None, **values):
    return invoke_structured(schema, template, fallback=fallback, **values)
