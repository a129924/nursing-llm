from __future__ import annotations

from pathlib import Path

from nursing_llm_server.applications.ports.llm.prompt_loader_abc import (
    PromptLoaderABC,
    PromptNotFoundError,
)
from nursing_llm_server.core.enums.role import Role
from nursing_llm_server.core.models.message import Message


class FilePromptLoader(PromptLoaderABC):
    def __init__(self, base_path: str | Path):
        self._base = Path(base_path)

    async def load_prompt(self, prompt_id: str) -> Message:
        path = self._base / f"prompt_{prompt_id}.md"

        if not path.exists():
            raise PromptNotFoundError(f"Prompt file not found: {path}")

        content = path.read_text(encoding="utf-8")

        return Message(role=Role.SYSTEM, content=content)
