from abc import ABC, abstractmethod
from typing import Generic, Protocol

from nursing_llm_server.core.types.generic import Entity, Schema
from nursing_llm_server.core.types.specific import PydanticModelProtocolType


class MapperInterface(Protocol[Schema, Entity]):  # type: ignore
    def schema_to_entity(self, schema: Schema) -> Entity: ...


class PydanticModelMapperABC(ABC, Generic[PydanticModelProtocolType, Entity]):
    @abstractmethod
    def schema_to_entity(self, schema: PydanticModelProtocolType) -> Entity:
        raise NotImplementedError(
            "Subclasses must implement the schema_to_entity method"
        )


class PydanticModelPayloadMapperABC(ABC, Generic[PydanticModelProtocolType, Entity]):
    @classmethod
    @abstractmethod
    def map_payload(cls, schema: PydanticModelProtocolType, payload: dict) -> Entity:
        raise NotImplementedError("Subclasses must implement the map_payload method")
