from nursing_llm_server.applications.exceptions.llm import ApplicationError


class ValidationError(ApplicationError):
    """Generic validation error."""
