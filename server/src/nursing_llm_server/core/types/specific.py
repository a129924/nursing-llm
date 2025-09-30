from typing import Any, Protocol, TypeVar


class PydanticModelProtocol(Protocol):
    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> "PydanticModelProtocol": ...

    @classmethod
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> "PydanticModelProtocol": ...


# Define Schema and Entity type variables for specific use
PydanticModelProtocolType = TypeVar(
    "PydanticModelProtocolType", bound=PydanticModelProtocol
)
