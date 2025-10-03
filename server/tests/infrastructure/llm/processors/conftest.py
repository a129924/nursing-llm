from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from nursing_llm_server.core.enums.role import Role
from nursing_llm_server.core.models.message import Message
from nursing_llm_server.core.models.stream_chunk import LLMStreamChunk
from nursing_llm_server.infrastructure.llm.processors.ollama_response_joiner import (
    OllamaResponseJoiner,
)


@pytest.fixture(scope="module")
def message_factory() -> Callable[[Role, str], Message]:
    def _factory(role: Role, content: str) -> Message:
        return Message(role=role, content=content)

    return _factory


@pytest.fixture(scope="module")
def stream_chunk_factory() -> Callable[
    [str, str, Message, bool, dict[str, Any] | None], LLMStreamChunk
]:
    def _factory(
        model: str,
        created_at: str,
        message: Message,
        done: bool = False,
        provider_raw: dict[str, Any] | None = None,
    ) -> LLMStreamChunk:
        return LLMStreamChunk(
            model=model,
            created_at=created_at,
            message=message,
            done=done,
            provider_raw=provider_raw,
        )

    return _factory


@pytest.fixture(scope="module")
def response_joiner() -> OllamaResponseJoiner:
    return OllamaResponseJoiner()
