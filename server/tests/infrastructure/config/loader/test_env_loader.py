from nursing_llm_server.infrastructure.config.loader.env_loader import EnvLoader


def test_env_loader(sample_env_loader: EnvLoader):
    config = sample_env_loader.load()
    assert config["TEST_ENV_VAR"] == "value"
    assert config["ANOTHER_TEST_VAR"] == "12345"
