from typing import cast

from typing_extensions import override

from nursing_llm_server.applications.ports.llm.llm_processor_abc import LLMProcessorABC
from nursing_llm_server.applications.validators.errors import ValidationError
from nursing_llm_server.applications.validators.pydantic.pydantic_validator import (
    PydanticValidator,
)
from nursing_llm_server.domain.entities.nursing import NursingNote
from nursing_llm_server.infrastructure.entities.nursing import NursingNoteSchema
from nursing_llm_server.infrastructure.llm.adapters.mappers.pydantic.nursing_mapper import (
    NursingMapper,
)
from nursing_llm_server.infrastructure.llm.schemas import OllamaResponseSchema


class OllamaProcessor(
    LLMProcessorABC[OllamaResponseSchema, NursingNoteSchema, NursingNote]
):
    def __init__(
        self,
        validator: PydanticValidator,
        payload_mapper: NursingMapper,
    ):
        self._validator = validator
        self._payload_mapper = payload_mapper

    @override
    def _validate_response(self, raw: str) -> OllamaResponseSchema:
        """Validate the outer response schema."""
        try:
            return cast(
                OllamaResponseSchema,
                self._validator.validate(OllamaResponseSchema, raw),
            )
        except ValidationError as e:
            from nursing_llm_server.infrastructure.llm.processors.errors.ollama import (
                OllamaResponseParserError,
            )

            raise OllamaResponseParserError(
                f"Ollama response validation error: {e}"
            ) from e

    @override
    def _validate_payload(
        self, response_schema: OllamaResponseSchema
    ) -> NursingNoteSchema:
        """Validate the payload schema."""
        try:
            return cast(
                NursingNoteSchema,
                self._validator.validate(NursingNoteSchema, response_schema.response),
            )
        except ValidationError as e:
            from nursing_llm_server.infrastructure.llm.processors.errors.nursing import (
                NursingPayloadParserError,
            )

            raise NursingPayloadParserError(
                f"Ollama payload validation error: {e}"
            ) from e

    @override
    def _payload_schema_to_entity(
        self, payload_schema: NursingNoteSchema
    ) -> NursingNote:
        """Map the payload schema to the entity."""
        return self._payload_mapper.schema_to_entity(payload_schema)
