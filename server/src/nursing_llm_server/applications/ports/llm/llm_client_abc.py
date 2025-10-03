from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from nursing_llm_server.core.models.message import Message
from nursing_llm_server.core.models.stream_chunk import LLMStreamChunk


class LLMClientABC(ABC):
    @abstractmethod
    async def stream_chat(
        self, messages: list[Message]
    ) -> AsyncIterator[LLMStreamChunk]:
        """Asynchronously stream chat responses as normalized LLMStreamChunk objects.

        Args:
            messages (list[Message]): 用於對話的消息列表。

        Yields:
            AsyncIterator[LLMStreamChunk]: provider-normalized stream chunks.
        """

    @abstractmethod
    async def chat(self, messages: list[Message]) -> str:
        """Convenience method that returns the full assembled chat response.

        Implementations MAY call `stream_chat` and join the chunks using a
        ResponseJoiner/strategy.
        """

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """根據輸入的提示詞生成回應。

        Args:
            prompt (str): 用於生成回應的提示詞。

        Returns:
            str: 生成的回應。
        """
        raise NotImplementedError("Subclasses must implement this method.")
