from pydantic import BaseModel


class BaseConfig(BaseModel):
    @classmethod
    def from_dict(cls, config_dict: dict) -> "BaseConfig":
        return cls(**config_dict)
