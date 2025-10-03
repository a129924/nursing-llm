from abc import ABC, abstractmethod

from nursing_llm_server.core.models.message import Message


class PromptNotFoundError(Exception):
    """Raised when a requested prompt cannot be found."""


class PromptLoaderABC(ABC):
    @abstractmethod
    async def load_prompt(self, prompt_id: str) -> Message:
        """Load a prompt content by id. Implementations may raise PromptNotFoundError.

        Returns the raw prompt string (e.g., markdown).
        """
        raise NotImplementedError
