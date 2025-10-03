from collections.abc import AsyncIterator

from nursing_llm_server.applications.ports.llm.response_joiner_abc import (
    ResponseJoinerABC,
)
from nursing_llm_server.core.models.stream_chunk import LLMStreamChunk


class OllamaResponseJoiner(ResponseJoinerABC):
    def _check_valid_stream(self, chunks: list[LLMStreamChunk]) -> bool:
        return bool(chunks) and chunks[-1].done is True

    async def collect(self, chunks: AsyncIterator[LLMStreamChunk]) -> dict:
        collected_content: list[LLMStreamChunk] = [chunk async for chunk in chunks]

        if not collected_content or not self._check_valid_stream(collected_content):
            from nursing_llm_server.infrastructure.llm.processors.errors.stream import (
                LLMStreamParseError,
            )

            raise LLMStreamParseError("Invalid stream chunk")

        content_response: str = "".join(
            chunk.message.content for chunk in collected_content
        )
        response_metadata = collected_content[-1].provider_raw or {}

        # Ensure "message" key exists and is a dict
        if "message" not in response_metadata or not isinstance(
            response_metadata["message"], dict
        ):
            response_metadata["message"] = {}

        response_metadata["message"]["content"] = content_response

        return response_metadata
