from __future__ import annotations

from collections.abc import AsyncIterator
from json import JSONDecodeError, loads
from typing import Any

from httpx import AsyncClient, ConnectTimeout, HTTPStatusError, ReadTimeout, Response
from typing_extensions import override

from nursing_llm_server.applications.ports.llm.llm_client_abc import LLMClientABC
from nursing_llm_server.core.enums.role import Role
from nursing_llm_server.core.models.message import Message
from nursing_llm_server.core.models.stream_chunk import LLMStreamChunk
from nursing_llm_server.infrastructure.config.ollama import OllamaConfig
from nursing_llm_server.infrastructure.llm.llm_client.errors import (
    LLMClientError,
    LLMJsonParseError,
    LLMNotFoundError,
    LLMRateLimitError,
    LLMTimeoutError,
)


class HttpxOllamaClient(LLMClientABC):
    def __init__(self, config: OllamaConfig, http_async_client: AsyncClient):
        self._config = config
        self._http_async_client = http_async_client

    async def _stream_response(
        self, response: Response
    ) -> AsyncIterator[LLMStreamChunk]:
        async for raw_chunk in response.aiter_text():
            text = raw_chunk.strip()
            if not text:
                continue

            # try parse JSON line, fall back to raw text
            try:
                parsed: dict[str, Any] = loads(text)
            except JSONDecodeError as json_decode_error:
                # if parser fails, continue to next chunk
                raise LLMJsonParseError(chunk=text) from json_decode_error

            # build Message and LLMStreamChunk from parsed dict
            msg_obj = parsed.get("message", {}) or {}
            role_str = (msg_obj.get("role") or "assistant").upper()
            try:
                role = Role[role_str]
            except Exception:
                role = Role.ASSISTANT

            content = msg_obj.get("content")

            yield LLMStreamChunk(
                model=parsed.get("model", self._config.model),
                created_at=parsed.get("created_at", ""),
                message=Message(role=role, content=content or ""),
                done=bool(parsed.get("done", False)),
                provider_raw=parsed,
            )

    @override
    async def stream_chat(
        self, messages: list[Message]
    ) -> AsyncIterator[LLMStreamChunk]:
        async with self._http_async_client.stream(
            "POST",
            f"{self._config.ollama_base_url}/chat",
            json={
                "messages": [
                    {
                        "role": message.role.name.lower(),
                        "content": message.content,
                    }
                    for message in messages
                ],
                "model": self._config.model,
            },
            timeout=self._config.timeout,
        ) as response:
            try:
                async for chunk in self._stream_response(response.raise_for_status()):
                    yield chunk

            except (ConnectTimeout, ReadTimeout) as timeout_error:
                raise LLMTimeoutError(
                    f"Request timed out: {timeout_error}"
                ) from timeout_error

            except HTTPStatusError as http_status_error:
                match http_status_error.response.status_code:
                    case 404:
                        raise LLMNotFoundError(
                            "Requested model/resource not found."
                        ) from http_status_error
                    case 429:
                        raise LLMRateLimitError(
                            "Rate limited by provider."
                        ) from http_status_error
                    case code if 400 <= code < 500:
                        raise LLMClientError(
                            f"Client error with status code {http_status_error.response.status_code}."
                        ) from http_status_error
                    case code if 500 <= code < 600:
                        raise LLMClientError(
                            f"Server error with status code {http_status_error.response.status_code}."
                        ) from http_status_error
                    case _:
                        raise LLMClientError(
                            f"Unexpected HTTP error with status code {http_status_error.response.status_code}."
                        ) from http_status_error

    @override
    async def chat(self, messages: list[Message]) -> str:
        # convenience helper: join streamed chunks into a single string
        return "".join(
            [
                chunk.message.content
                async for chunk in self.stream_chat(messages)
                if chunk.message and chunk.message.content
            ]
        )

    @override
    async def generate(self, prompt: str) -> str:
        # 使用 httpx 發送請求到 Ollama 伺服器並返回生成的回應
        try:
            response = await self._http_async_client.post(
                f"{self._config.ollama_base_url}/generate",
                json={
                    "prompt": prompt,
                    "model": self._config.model,
                },
            )

            return response.raise_for_status().text
        except (ConnectTimeout, ReadTimeout) as timeout_error:
            raise LLMTimeoutError(
                f"Request timed out: {timeout_error}"
            ) from timeout_error

        except HTTPStatusError as http_status_error:
            match http_status_error.response.status_code:
                case 404:
                    raise LLMNotFoundError(
                        "Requested model/resource not found."
                    ) from http_status_error
                case 429:
                    raise LLMRateLimitError(
                        "Rate limited by provider."
                    ) from http_status_error
                case code if 400 <= code < 500:
                    raise LLMClientError(
                        f"Client error with status code {http_status_error.response.status_code}."
                    ) from http_status_error
                case code if 500 <= code < 600:
                    raise LLMClientError(
                        f"Server error with status code {http_status_error.response.status_code}."
                    ) from http_status_error
                case _:
                    raise LLMClientError(
                        f"Unexpected HTTP error with status code {http_status_error.response.status_code}."
                    ) from http_status_error
