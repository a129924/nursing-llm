from collections.abc import AsyncIterator

from nursing_llm_server.applications.ports.llm.response_joiner_abc import (
    ResponseJoinerABC,
)
from nursing_llm_server.core.models.stream_chunk import LLMStreamChunk


class OllamaResponseJoiner(ResponseJoinerABC):
    async def collect(self, chunks: AsyncIterator[LLMStreamChunk]) -> dict:
        collected_content = [chunk async for chunk in chunks]

        if not collected_content:
            return {}

        content_response: str = "".join(
            chunk.message.content for chunk in collected_content[:-1]
        )
        metadata = collected_content[-1].provider_raw or {}

        # Ensure 'message' key exists in metadata
        if "message" not in metadata or not isinstance(metadata["message"], dict):
            metadata["message"] = {}

        metadata["message"]["content"] = content_response

        return metadata
