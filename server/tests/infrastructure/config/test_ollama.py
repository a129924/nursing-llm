from nursing_llm_server.infrastructure.config.loader.env_loader import EnvLoader
from nursing_llm_server.infrastructure.config.ollama import OllamaConfig


def test_ollama_config_from_env_file(ollama_config_loader: EnvLoader):
    config_data = ollama_config_loader.load()

    assert config_data["host"] == "http://localhost"
    assert config_data["port"] == "11434"
    assert config_data["model"] == "ggml-llama2-7b"
    assert config_data["timeout"] == "30"
    assert config_data.get("api_key", None) is None


def test_ollama_config_instance(
    sample_ollama_config_instance: OllamaConfig,
    sample_ollama_config,
):
    assert sample_ollama_config_instance.host == sample_ollama_config["host"]
    assert sample_ollama_config_instance.port == sample_ollama_config["port"]
    assert sample_ollama_config_instance.model == sample_ollama_config["model"]
    assert sample_ollama_config_instance.timeout == sample_ollama_config["timeout"]
    assert sample_ollama_config_instance.api_key == sample_ollama_config["api_key"]

    assert (
        sample_ollama_config_instance.base_url
        == f"{sample_ollama_config_instance.host}:{sample_ollama_config_instance.port}"
    )
