from collections.abc import Iterator
from json import JSONDecodeError, loads
from pathlib import Path

from typing_extensions import override

from nursing_llm_server.applications.ports.llm.message_loader_abc import (
    MessageLoaderABC,
)
from nursing_llm_server.core.enums.role import Role
from nursing_llm_server.core.models.message import Message
from nursing_llm_server.infrastructure.llm.adapters.message_loader.errors import (
    MessageFileNotFoundError,
    MessageParseError,
    MessageSchemaError,
)


class JSONMessageLoader(MessageLoaderABC):
    def __init__(self, base_dir: str):
        self._base_dir = Path(base_dir)

    def _is_valid_message_schema(self, item: dict[str, str]) -> bool:
        return isinstance(item, dict) and "role" in item and "content" in item

    def _process_parsed(self, parsed: list[dict[str, str]]) -> Iterator[Message]:
        for item in parsed:
            if not self._is_valid_message_schema(item):
                raise MessageSchemaError(f"Invalid message schema: {item}")

            try:
                role = Role[item["role"].upper()]
            except KeyError:
                raise MessageSchemaError(
                    f"Invalid role value: {item['role']}"
                ) from KeyError
            content = item["content"]

            yield Message(role=role, content=content)

    @override
    async def load_messages(self, message_id: str) -> list[Message]:
        # Load messages from a JSON source identified by message_id
        try:
            raw = (self._base_dir / f"message_{message_id}.json").read_text(
                encoding="utf-8"
            )

            parsed: list[dict[str, str]] | dict[str, str] = loads(raw)

        except FileNotFoundError as fnf_error:
            raise MessageFileNotFoundError(
                f"Message file not found: {self._base_dir / f'{message_id}.json'}"
            ) from fnf_error

        except JSONDecodeError as e:
            raise MessageParseError(f"Invalid JSON messages: {e}") from e

        if isinstance(parsed, dict):
            # single message dict, wrap in list
            parsed = [parsed]

        return list(self._process_parsed(parsed))
