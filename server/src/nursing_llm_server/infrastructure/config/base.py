from functools import cached_property

from pydantic import BaseModel, ConfigDict


class BaseConfig(BaseModel):
    @classmethod
    def from_dict(cls, config_dict: dict) -> "BaseConfig":
        return cls(**config_dict)


class AIConfig(BaseConfig):
    model: str
    temperature: float
    max_tokens: int
    top_p: float
    seed: int
    host: str
    port: int
    timeout: int
    api_key: str | None = None

    @cached_property
    def base_url(self) -> str:
        return f"{self.host}:{self.port}"

    model_config = ConfigDict(frozen=True)
