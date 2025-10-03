from abc import ABC, abstractmethod
from typing import Any, Generic

from nursing_llm_server.core.types.generic import Entity, PayloadSchema, ResponseSchema


class LLMProcessorABC(ABC, Generic[ResponseSchema, PayloadSchema, Entity]):
    # validation method
    @abstractmethod
    def _validate_response(self, raw: str | dict[str, Any]) -> ResponseSchema:
        """Validate the outer response schema."""
        raise NotImplementedError(
            "Subclasses must implement the _validate_response method"
        )

    @abstractmethod
    def _validate_payload(self, response_schema: ResponseSchema) -> PayloadSchema:
        """Validate the payload schema."""
        raise NotImplementedError(
            "Subclasses must implement the _validate_payload method"
        )

    # mapping method
    @abstractmethod
    def _payload_schema_to_entity(self, payload_schema: PayloadSchema) -> Entity:
        """Map the payload schema to the entity."""
        raise NotImplementedError(
            "Subclasses must implement the _payload_schema_to_entity method"
        )

    def validate_and_map(self, raw: str | dict[str, Any]) -> Entity:
        # Full processing method
        ## Step 1: Validate the outer response schema
        response_schema = self._validate_response(raw)
        ## Step 2: Validate the payload schema
        payload_schema = self._validate_payload(response_schema)
        ## Step 3: Map the payload schema to the entity
        entity = self._payload_schema_to_entity(payload_schema)

        return entity
