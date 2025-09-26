from functools import cached_property

from pydantic import ConfigDict, computed_field

from nursing_llm_server.infrastructure.config.base import BaseConfig


class OllamaConfig(BaseConfig):
    host: str = "http://localhost"
    port: int = 11434
    model: str = "ggml-llama2-7b"  # 預設模型
    timeout: int = 30  # 請求超時時間（秒）
    api_key: str | None = None  # 如果有認證 token，可以放這裡

    model_config = ConfigDict(frozen=True)

    @computed_field
    @cached_property
    def ollama_base_url(self) -> str:
        return f"{self.host}:{self.port}"
