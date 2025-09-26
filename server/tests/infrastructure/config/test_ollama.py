from nursing_llm_server.infrastructure.config.loader.env_loader import EnvLoader


def test_ollama_config_from_env_file(ollama_config_loader: EnvLoader):
    config_data = ollama_config_loader.load()

    assert config_data["host"] == "http://localhost"
    assert config_data["port"] == "11434"
    assert config_data["model"] == "ggml-llama2-7b"
    assert config_data["timeout"] == "30"
    assert config_data.get("api_key", None) is None
