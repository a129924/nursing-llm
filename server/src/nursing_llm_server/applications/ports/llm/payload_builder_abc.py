from __future__ import annotations

from abc import ABC, abstractmethod

from nursing_llm_server.core.models.message import Message
from nursing_llm_server.core.models.payload import Payload


class PayloadBuilderABC(ABC):
    @abstractmethod
    def build_chat_payload(self, messages: list[Message]) -> Payload:
        """Build a provider-specific request body for chat operations.

        `overrides` can contain per-call options such as model, stream, or other
        provider specific flags.
        """
        raise NotImplementedError
