from nursing_llm_server.infrastructure.llm.processors.errors import ParserError


class LLMStreamParseError(ParserError):
    """Raised when a stream chunk from LLM provider is invalid or unparsable."""
