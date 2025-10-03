from nursing_llm_server.infrastructure.config.ollama import OllamaConfig
from nursing_llm_server.infrastructure.llm.adapters.url_builder.ollama_url_builder import (
    OllamaUrlBuilder,
)


def build_minimal_config(**overrides):
    # Provide the numeric fields required by AIConfig base
    defaults = {
        "temperature": 0.5,
        "max_tokens": 128,
        "top_p": 0.9,
        "seed": 0,
    }
    defaults.update(overrides)
    return OllamaConfig(**defaults)


def test_default_urls() -> None:
    cfg = build_minimal_config()
    builder = OllamaUrlBuilder(cfg)

    assert builder.build_chat_url() == "http://localhost:11434/chat"
    assert builder.build_generate_url() == "http://localhost:11434/generate"
    assert builder.build_health_url() == "http://localhost:11434/health"


def test_custom_host_and_port() -> None:
    cfg = build_minimal_config(host="http://example.com", port=8000)
    builder = OllamaUrlBuilder(cfg)

    assert builder.build_chat_url() == "http://example.com:8000/chat"


def test_preserve_existing_path() -> None:
    cfg = build_minimal_config(host="http://example.com/base", port=8000)
    builder = OllamaUrlBuilder(cfg)

    url = builder.build_chat_url()
    assert url.endswith("/chat")
    assert "/base" in url
