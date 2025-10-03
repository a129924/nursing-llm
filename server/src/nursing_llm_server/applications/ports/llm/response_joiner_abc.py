from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from nursing_llm_server.core.models.stream_chunk import LLMStreamChunk


class ResponseJoinerABC(ABC):
    @abstractmethod
    async def collect(self, chunks: AsyncIterator[LLMStreamChunk]) -> dict:
        """Collect streamed chunks and assemble a final response.

        Returns a tuple of (assembled_text, metadata). Metadata is a provider-agnostic
        dict that may include diagnostic/provider information.
        """
