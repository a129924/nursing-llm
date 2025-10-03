from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from nursing_llm_server.core.enums.role import Role
from nursing_llm_server.core.models.message import Message


@dataclass(frozen=True)
class LLMStreamChunk:
    """Represents a single chunk from an LLM streaming response.

    Fields are intentionally optional/lightweight so different providers can populate
    the subset they support. Keep this in core so application/infra share the type.
    """

    model: str
    created_at: str
    message: Message
    done: bool
    # raw provider-specific payload for callers that need deep inspection
    provider_raw: dict[str, Any] | None = None
