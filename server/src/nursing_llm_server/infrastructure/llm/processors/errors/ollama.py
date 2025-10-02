from nursing_llm_server.infrastructure.llm.processors.errors import ParserError


class OllamaResponseParserError(ParserError):
    """Raised when outer Ollama response (outer schema) is invalid or unparsable."""
