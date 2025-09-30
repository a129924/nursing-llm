class ApplicationError(Exception):
    """Base application-level exception."""


class LLMClientError(ApplicationError):
    """Generic LLM client error (network/infra)."""


class LLMRateLimitError(LLMClientError):
    """Rate limited by provider."""


class LLMNotFoundError(LLMClientError):
    """Requested model/resource not found."""


class LLMTimeoutError(LLMClientError):
    """Request to LLM provider timed out."""
