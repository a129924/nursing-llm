from json import dumps

from pytest import raises

from nursing_llm_server.domain.entities.nursing import NursingNote
from nursing_llm_server.infrastructure.llm.processors.errors.nursing import (
    NursingPayloadParserError,
)
from nursing_llm_server.infrastructure.llm.processors.errors.ollama import (
    OllamaResponseParserError,
)
from nursing_llm_server.infrastructure.llm.processors.ollama_chat_processor import (
    OllamaChatProcessor,
)


def build_chat_response(model: str, message_content: str, done: bool = True) -> str:
    return dumps(
        {
            "model": model,
            "created_at": "2025-10-01T08:44:25.304513Z",
            "message": {"role": "assistant", "content": message_content},
            "done": done,
            "done_reason": "stop",
            "total_duration": 0.0,
            "load_duration": 0.0,
            "prompt_eval_count": 0,
            "prompt_eval_duration": 0.0,
            "eval_count": 0,
            "eval_duration": 0.0,
        }
    )


def test_ollama_chat_processor_happy_path(
    pydantic_validator, nursing_mapper, nursing_record_json
) -> None:
    """驗證正常 chat 回應能被驗證、解析並映射為 domain entity"""
    processor = OllamaChatProcessor(
        validator=pydantic_validator, payload_mapper=nursing_mapper
    )

    chat_json = build_chat_response("llama2:7b-chat", nursing_record_json)

    result = processor.validate_and_map(chat_json)

    assert isinstance(result, NursingNote)
    assert result is not None


def test_ollama_chat_processor_invalid_outer_raises(
    pydantic_validator, nursing_mapper
) -> None:
    """當 outer schema 不正確時，應拋出 OllamaResponseParserError"""
    processor = OllamaChatProcessor(
        validator=pydantic_validator, payload_mapper=nursing_mapper
    )

    # missing `message` key
    bad_outer = dumps(
        {
            "model": "llama2:7b-chat",
            "created_at": "2025-10-01T08:44:25.304513Z",
            "done": True,
            "done_reason": "stop",
            "total_duration": 0.0,
            "load_duration": 0.0,
            "prompt_eval_count": 0,
            "prompt_eval_duration": 0.0,
            "eval_count": 0,
            "eval_duration": 0.0,
        }
    )

    with raises(OllamaResponseParserError):
        processor.validate_and_map(bad_outer)


def test_ollama_chat_processor_invalid_inner_payload_raises(
    pydantic_validator, nursing_mapper
) -> None:
    """當 message.content 不是合法 nursing payload 時，應拋出 NursingPayloadParserError"""
    processor = OllamaChatProcessor(
        validator=pydantic_validator, payload_mapper=nursing_mapper
    )

    # message.content 不是合法的 nursing json
    chat_with_bad_payload = build_chat_response("llama2:7b-chat", "not a json")

    with raises(NursingPayloadParserError):
        processor.validate_and_map(chat_with_bad_payload)


def test_ollama_chat_processor_raw_dict_happy_path(
    pydantic_validator, nursing_mapper, nursing_record_json
) -> None:
    """當 raw 為 dict（非 JSON 字串）時，processor 應能正常處理並回傳 entity"""
    processor = OllamaChatProcessor(
        validator=pydantic_validator, payload_mapper=nursing_mapper
    )

    chat_dict = {
        "model": "llama2:7b-chat",
        "created_at": "2025-10-01T08:44:25.304513Z",
        "message": {"role": "assistant", "content": nursing_record_json},
        "done": True,
        "done_reason": "stop",
        "total_duration": 0.0,
        "load_duration": 0.0,
        "prompt_eval_count": 0,
        "prompt_eval_duration": 0.0,
        "eval_count": 0,
        "eval_duration": 0.0,
    }

    result = processor.validate_and_map(chat_dict)

    assert isinstance(result, NursingNote)
    assert result is not None
