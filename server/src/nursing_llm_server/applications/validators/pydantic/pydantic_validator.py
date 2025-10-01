from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from typing_extensions import override

from nursing_llm_server.applications.validators.errors import ValidationError
from nursing_llm_server.core.shared.validation import PydanticModelValidatorABC


class PydanticValidator(PydanticModelValidatorABC):
    @override
    @classmethod
    def validate(cls, validate_schema: type[BaseModel], raw: str) -> BaseModel:
        try:
            return validate_schema.model_validate_json(raw)
        except PydanticValidationError as e:
            raise ValidationError(f"Validation error: {e}") from e
