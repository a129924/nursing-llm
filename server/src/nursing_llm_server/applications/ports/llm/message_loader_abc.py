from __future__ import annotations

from abc import ABC, abstractmethod

from nursing_llm_server.core.models.message import Message


class MessageLoadError(Exception):
    """Raised when messages cannot be loaded or parsed."""

    pass


class MessageLoaderABC(ABC):
    @abstractmethod
    async def load_messages(self, message_id: str) -> list[Message]:
        """Load and parse messages from a source identified by message_id."""
        raise NotImplementedError
