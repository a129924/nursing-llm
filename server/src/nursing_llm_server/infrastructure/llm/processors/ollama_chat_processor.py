from typing import Any, cast

from typing_extensions import override

from nursing_llm_server.applications.ports.llm.llm_processor_abc import (
    LLMProcessorABC,
)
from nursing_llm_server.applications.validators.errors import ValidationError
from nursing_llm_server.applications.validators.pydantic.pydantic_validator import (
    PydanticValidator,
)
from nursing_llm_server.domain.entities.nursing import NursingNote
from nursing_llm_server.infrastructure.entities.nursing import NursingNoteSchema
from nursing_llm_server.infrastructure.llm.adapters.mappers.pydantic.nursing_mapper import (
    NursingMapper,
)
from nursing_llm_server.infrastructure.llm.schemas import (
    OllamaChatMessageSchema,
    OllamaChatResponseSchema,
)


class OllamaChatProcessor(
    LLMProcessorABC[OllamaChatResponseSchema, OllamaChatMessageSchema, NursingNote]
):
    """
    Processor for Ollama chat responses.

    - 驗證 outer chat response (OllamaChatResponseSchema)
    - 從 outer 取出 message 並驗證為 OllamaChatMessageSchema
    - 將 payload map 成 domain entity (NursingNote) via injected mapper
    """

    def __init__(self, validator: PydanticValidator, payload_mapper: NursingMapper):
        self._validator = validator
        self._payload_mapper = payload_mapper

    @override
    def _validate_response(self, raw: str | dict[str, Any]) -> OllamaChatResponseSchema:
        """Validate the outer chat response (per-line or assembled)."""
        try:
            return cast(
                OllamaChatResponseSchema,
                self._validator.validate(OllamaChatResponseSchema, raw),
            )
        except ValidationError as e:
            from nursing_llm_server.infrastructure.llm.processors.errors.ollama import (
                OllamaResponseParserError,
            )

            raise OllamaResponseParserError(
                f"Ollama chat response validation error: {e}"
            ) from e

    @override
    def _validate_payload(
        self, response_schema: OllamaChatResponseSchema
    ) -> NursingNoteSchema:
        """Validate the inner `message` payload."""
        try:
            # response_schema.message may already be a BaseModel instance; convert to plain dict
            return cast(
                NursingNoteSchema,
                self._validator.validate(
                    NursingNoteSchema, response_schema.message.content
                ),
            )
        except ValidationError as e:
            # reuse nursing payload error type for now (or replace with a chat-specific error)
            from nursing_llm_server.infrastructure.llm.processors.errors.nursing import (
                NursingPayloadParserError,
            )

            raise NursingPayloadParserError(
                f"Ollama chat payload validation error: {e}"
            ) from e

    @override
    def _payload_schema_to_entity(
        self, payload_schema: NursingNoteSchema
    ) -> NursingNote:
        """Map the validated message payload to a domain entity."""
        return self._payload_mapper.schema_to_entity(payload_schema)
