from typing_extensions import override

from nursing_llm_server.applications.ports.llm.message_loader_abc import (
    MessageLoaderABC,
)
from nursing_llm_server.applications.ports.llm.prompt_loader_abc import (
    PromptLoaderABC,
)
from nursing_llm_server.core.enums.role import Role
from nursing_llm_server.core.models.message import Message


class MemoryPromptLoader(PromptLoaderABC):
    """A simple in-memory async prompt loader for tests.

    Provide a dict mapping prompt_id -> prompt_content when constructing.
    """

    def __init__(self, prompts: str) -> None:
        self._prompts = prompts

    async def load_prompt(self, prompt_id: str) -> Message:
        return Message(role=Role.SYSTEM, content=self._prompts)


class MemoryMessageLoader(MessageLoaderABC):
    """A test message loader that reads from an in-memory mapping or accepts raw lists/JSON.

    Usage patterns in tests:
    - Pass a key string as `raw` that exists in `mapping` to return prebuilt messages.
    - Pass a JSON string or iterable[dict] to parse live.
    """

    def __init__(self, messages: list[Message]) -> None:
        self._messages = messages

    @override
    async def load_messages(self, message_id: str) -> list[Message]:
        return self._messages


# convenience fixtures factories for tests
def make_memory_prompt_loader(prompts: str) -> MemoryPromptLoader:
    return MemoryPromptLoader(prompts=prompts)


def make_memory_message_loader(
    messages: list[Message],
) -> MemoryMessageLoader:
    return MemoryMessageLoader(messages=messages)
