from urllib.parse import urlparse, urlunparse

from nursing_llm_server.applications.ports.llm.url_builder_abc import (
    AIPlatformUrlBuilderABC,
)
from nursing_llm_server.infrastructure.config.ollama import OllamaConfig


class OllamaUrlBuilder(AIPlatformUrlBuilderABC):
    """
    OllamaUrlBuilder constructs URLs for interacting with the Ollama LLM platform.

    Args:
        config (OllamaConfig): Configuration object containing the base URL for the Ollama service.
    """

    def __init__(self, config: OllamaConfig):
        self._config = config

    def build_chat_url(self) -> str:
        parsed = urlparse(self._config.base_url)
        # Ensure the path ends with /chat, preserving any existing path
        new_path = parsed.path.rstrip("/") + "/chat"
        new_url = parsed._replace(path=new_path)

        return urlunparse(new_url)

    def build_generate_url(self) -> str:
        parsed = urlparse(self._config.base_url)
        # Ensure the path ends with /generate, preserving any existing path
        new_path = parsed.path.rstrip("/") + "/generate"
        new_url = parsed._replace(path=new_path)

        return urlunparse(new_url)

    def build_health_url(self) -> str:
        parsed = urlparse(self._config.base_url)
        # Ensure the path ends with /health, preserving any existing path
        new_path = parsed.path.rstrip("/") + "/health"
        new_url = parsed._replace(path=new_path)

        return urlunparse(new_url)
