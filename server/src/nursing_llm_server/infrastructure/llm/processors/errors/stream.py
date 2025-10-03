from nursing_llm_server.infrastructure.llm.processors.errors import ParserError


class LLMStreamParseError(ParserError):
    """Raised when streamed chunks cannot be parsed/assembled to a valid response."""
