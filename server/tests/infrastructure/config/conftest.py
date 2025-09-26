from collections.abc import Generator
from io import TextIOBase

from pytest import fixture

from nursing_llm_server.infrastructure.config.loader.env_loader import EnvLoader
from nursing_llm_server.infrastructure.config.ollama import OllamaConfig
from tests.helpers import get_abs_path


@fixture(scope="module")
def sample_ollama_config() -> dict:
    return {
        "host": "http://localhost",
        "port": 11434,
        "model": "ollama/llama-2-7b",
        "timeout": 60,
        "api_key": None,
    }


@fixture(scope="module")
def sample_ollama_config_path() -> str:
    return get_abs_path("tests/mock/files/test_ollama_config.env", from_server=True)


@fixture(scope="module")
def sample_env_file_path() -> str:
    return get_abs_path("tests/mock/files/test.env", from_server=True)


@fixture(scope="function")
def sample_env_text_io_base(
    sample_env_file_path: str,
) -> Generator[TextIOBase, None, None]:
    with open(sample_env_file_path, encoding="utf-8") as f:
        yield f


@fixture(scope="function")
def ollama_env_text_io_base(
    sample_ollama_config_path: str,
) -> Generator[TextIOBase, None, None]:
    with open(sample_ollama_config_path, encoding="utf-8") as f:
        yield f


@fixture(scope="function")
def sample_env_loader(sample_env_text_io_base: TextIOBase) -> EnvLoader:
    from nursing_llm_server.infrastructure.config.loader.env_loader import EnvLoader

    return EnvLoader(sample_env_text_io_base)


@fixture(scope="function")
def ollama_config_loader(ollama_env_text_io_base: TextIOBase) -> EnvLoader:
    return EnvLoader(ollama_env_text_io_base)


@fixture(scope="module")
def sample_ollama_config_instance(sample_ollama_config: dict) -> OllamaConfig:
    return OllamaConfig(**sample_ollama_config)
