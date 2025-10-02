from nursing_llm_server.infrastructure.llm.processors.errors import ParserError


class NursingPayloadParserError(ParserError):
    """Raised when inner nursing JSON payload is invalid or unparsable."""
