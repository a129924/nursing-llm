from pydantic import BaseModel
from typing_extensions import override

from nursing_llm_server.core.shared.validation import PydanticModelValidatorABC


class PydanticValidator(PydanticModelValidatorABC):
    @override
    @classmethod
    def validate(cls, validate_schema: type[BaseModel], raw: str) -> BaseModel:
        return validate_schema.model_validate_json(raw)
