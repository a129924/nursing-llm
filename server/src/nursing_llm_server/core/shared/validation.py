from abc import ABC, abstractmethod
from typing import Any, Generic

from nursing_llm_server.core.types.generic import Schema
from nursing_llm_server.core.types.specific import PydanticModelProtocol


class ModelValidator(Generic[Schema], ABC):
    @classmethod
    @abstractmethod
    def validate(cls, validate_schema: type[Schema], raw: Any) -> Schema:
        raise NotImplementedError("Subclasses must implement the validate method")


class PydanticModelValidatorABC(ABC):
    @classmethod
    @abstractmethod
    def validate(
        cls, validate_schema: type[PydanticModelProtocol], raw: str
    ) -> PydanticModelProtocol:
        raise NotImplementedError("Subclasses must implement the validate method")
