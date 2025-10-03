from __future__ import annotations

from nursing_llm_server.applications.ports.llm.prompt_loader_abc import PromptLoaderABC
from nursing_llm_server.infrastructure.llm.adapters.prompt_loader.file_prompt_loader import (
    FilePromptLoader,
)


class PromptLoaderFactory:
    @staticmethod
    def get(source: str, **kwargs) -> PromptLoaderABC:
        """Return a PromptLoader implementation based on source.

        source: 'file' | 'redis' | 'db'
        kwargs: passed to loader constructor (e.g., base_path)
        """
        if source == "file":
            return FilePromptLoader(kwargs.get("base_path", "."))

        raise ValueError(f"Unknown prompt loader source: {source}")
