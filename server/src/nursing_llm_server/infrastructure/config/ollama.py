from nursing_llm_server.infrastructure.config.base import AIConfig


class OllamaConfig(AIConfig):
    host: str = "http://localhost"
    port: int = 11434
    model: str = "ggml-llama2-7b"  # 預設模型
    timeout: int = 30  # 請求超時時間（秒）
    api_key: str | None = None  # 如果有認證 token，可以放這裡
