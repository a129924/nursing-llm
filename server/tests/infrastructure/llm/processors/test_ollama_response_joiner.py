from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from typing import TYPE_CHECKING

from pytest import mark, raises

from nursing_llm_server.core.enums.role import Role
from nursing_llm_server.infrastructure.llm.processors.errors.stream import (
    LLMStreamParseError,
)

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


async def _aiter_with_raise(
    items: list[LLMStreamChunk], raise_at_index: int, exc: Exception
) -> AsyncIterator[LLMStreamChunk]:
    for idx, it in enumerate(items):
        if idx == raise_at_index:
            raise exc
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
    assert assembled.get("message", {}).get("content") == "Hello world"


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
    assert assembled.get("message", {}).get("content") == "User text continuation"


@mark.asyncio
async def test_collect_empty_stream(response_joiner: OllamaResponseJoiner) -> None:
    with raises(LLMStreamParseError):
        await response_joiner.collect(_aiter_from_list([]))


@mark.asyncio
async def test_joiner_transport_error_propagates(
    response_joiner: OllamaResponseJoiner, stream_chunk_factory, message_factory
) -> None:
    # Simulate transport-layer exception during iteration
    transport_exc = RuntimeError("connection reset")

    chunk1 = stream_chunk_factory(
        "llama2:7b-chat",
        "2025-10-01T08:44:25.304513Z",
        message_factory(Role.ASSISTANT, "Hello"),
        done=False,
        provider_raw=None,
    )

    # The iterator will raise when encountering the index
    with raises(LLMStreamParseError):
        await response_joiner.collect(_aiter_with_raise([chunk1], 1, transport_exc))


@mark.asyncio
async def test_joiner_incomplete_stream_raises(
    stream_chunk_factory, message_factory, response_joiner: OllamaResponseJoiner
):
    # Last chunk done=False
    chunk1 = stream_chunk_factory(
        "llama2:7b-chat",
        "2025-10-01T08:44:25.304513Z",
        message_factory(Role.ASSISTANT, "part1"),
        done=False,
        provider_raw=None,
    )
    chunk2 = stream_chunk_factory(
        "llama2:7b-chat",
        "2025-10-01T08:44:26.304513Z",
        message_factory(Role.ASSISTANT, "part2"),
        done=False,
        provider_raw={"model": "llama2:7b-chat"},
    )

    with raises(LLMStreamParseError):
        await response_joiner.collect(
            _aiter_with_raise([chunk1, chunk2], 999, RuntimeError("won't be used"))
        )
