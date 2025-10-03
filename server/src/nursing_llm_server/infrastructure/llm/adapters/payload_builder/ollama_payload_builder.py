from collections.abc import AsyncGenerator

from typing_extensions import override

from nursing_llm_server.applications.ports.llm.message_loader_abc import (
    MessageLoaderABC,
)
from nursing_llm_server.applications.ports.llm.payload_builder_abc import (
    PayloadBuilderABC,
)
from nursing_llm_server.applications.ports.llm.prompt_loader_abc import PromptLoaderABC
from nursing_llm_server.core.enums.role import Role
from nursing_llm_server.core.models.message import Message
from nursing_llm_server.core.models.payload import Payload
from nursing_llm_server.infrastructure.config.ollama import OllamaConfig


class OllamaPayloadBuilder(PayloadBuilderABC):
    def __init__(
        self,
        config: OllamaConfig,
        prompt_loader: PromptLoaderABC,
        message_loader: MessageLoaderABC,
    ):
        self._config = config
        self._prompt_loader = prompt_loader
        self._message_loader = message_loader

    @override
    def build_chat_payload(self, messages: list[Message]) -> Payload:
        return Payload(
            model=self._config.model,
            messages=messages,
            stream=True,
            options={
                "temperature": self._config.temperature,
                "top_p": self._config.top_p,
                "max_tokens": self._config.max_tokens,
                "seed": self._config.seed,
            },
        )

    async def _build_chat_payload_from_user(
        self,
        user_input: str,
        prompt_id: str,
        example_id: str,
    ) -> AsyncGenerator[Message, None]:
        prompt_message = await self._prompt_loader.load_prompt(prompt_id)

        # wrap the loaded prompt string into a system Message
        yield prompt_message

        for few_example_message in await self._message_loader.load_messages(example_id):
            yield few_example_message

        yield Message(role=Role.USER, content=user_input)

    async def build_chat_payload_from_user(
        self,
        user_input: str,
        prompt_id: str,
        example_id: str,
    ) -> Payload:
        """Build payload from a user's input, optionally loading a system prompt and messages from sources.

        - prompt_source: which loader factory source to use (e.g., 'file')
        - prompt_id: identifier for the prompt file (without extension)
        - messages_raw: raw JSON string or iterable that MessageLoader can parse
        """
        messages = [
            m
            async for m in self._build_chat_payload_from_user(
                user_input=user_input,
                prompt_id=prompt_id,
                example_id=example_id,
            )
        ]

        return self.build_chat_payload(messages=messages)
