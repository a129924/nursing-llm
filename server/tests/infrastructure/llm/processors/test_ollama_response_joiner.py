from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from typing import TYPE_CHECKING

from pytest import mark

from nursing_llm_server.core.enums.role import Role

if TYPE_CHECKING:
    from nursing_llm_server.core.models.message import Message
    from nursing_llm_server.core.models.stream_chunk import LLMStreamChunk
    from nursing_llm_server.infrastructure.llm.processors.ollama_response_joiner import (
        OllamaResponseJoiner,
    )


async def _aiter_from_list(
    items: list[LLMStreamChunk],
) -> AsyncIterator[LLMStreamChunk]:
    for it in items:
        yield it


@mark.asyncio
async def test_collect_simple(
    response_joiner: OllamaResponseJoiner,
    stream_chunk_factory: Callable[..., LLMStreamChunk],
    message_factory: Callable[[Role, str], Message],
) -> None:
    msg1 = message_factory(Role.ASSISTANT, "Hello")
    msg2 = message_factory(Role.ASSISTANT, " world")

    chunk1 = stream_chunk_factory(
        "llama2:7b-chat",
        "2025-10-01T08:44:25.304513Z",
        msg1,
        done=False,
        provider_raw=None,
    )
    # last chunk provides provider_raw metadata
    chunk2 = stream_chunk_factory(
        "llama2:7b-chat",
        "2025-10-01T08:44:26.304513Z",
        msg2,
        done=True,
        provider_raw={
            "model": "llama2:7b-chat",
            "message": {"role": "assistant", "content": ""},
            "done": True,
        },
    )

    assembled = await response_joiner.collect(_aiter_from_list([chunk1, chunk2]))

    assert isinstance(assembled, dict)
    assert assembled.get("message", {}).get("content") == "Hello"


@mark.asyncio
async def test_collect_message_variants(
    response_joiner: OllamaResponseJoiner,
    stream_chunk_factory: Callable[..., LLMStreamChunk],
    message_factory: Callable[[Role, str], Message],
) -> None:
    # variant: role as USER
    msg1 = message_factory(Role.USER, "User text")
    chunk1 = stream_chunk_factory(
        "llama2:7b-chat",
        "2025-10-01T08:44:25.304513Z",
        msg1,
        done=False,
        provider_raw=None,
    )

    # variant: provider_raw missing message key
    chunk2 = stream_chunk_factory(
        "llama2:7b-chat",
        "2025-10-01T08:44:26.304513Z",
        message_factory(Role.ASSISTANT, " continuation"),
        done=True,
        provider_raw={"model": "llama2:7b-chat", "done": True},
    )

    assembled = await response_joiner.collect(_aiter_from_list([chunk1, chunk2]))

    assert isinstance(assembled, dict)
    # content should be concatenation of all but the last chunk
    assert assembled.get("message", {}).get("content") == "User text"


@mark.asyncio
async def test_collect_empty_stream(response_joiner: OllamaResponseJoiner) -> None:
    assembled = await response_joiner.collect(_aiter_from_list([]))

    assert assembled == {}
