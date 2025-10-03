from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from nursing_llm_server.core.models.message import Message


@dataclass(frozen=True)
class Payload:
    """Provider-agnostic payload representing a chat request to an LLM.

    Stored in core so application/infra can share the same contract.
    """

    model: str
    messages: list[Message]
    stream: bool = False
    options: Mapping[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to a plain dict suitable for JSON serialization by infra clients.

        - role is emitted as a lowercase string (e.g. "user", "assistant", "system").
        - metadata is converted to a dict if present.
        - options becomes an empty dict when None to simplify infra logic.
        """
        return {
            "model": self.model,
            "messages": [
                {
                    "role": message.role.name.lower(),
                    "content": message.content,
                }
                for message in self.messages
            ],
            "stream": self.stream,
            "options": dict(self.options) if self.options is not None else {},
        }
