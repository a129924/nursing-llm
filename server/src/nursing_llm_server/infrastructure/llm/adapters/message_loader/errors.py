class MessageLoaderError(Exception):
    """Base exception for message loader problems."""


class MessageParseError(MessageLoaderError):
    """Raised when parsing of messages fails (invalid format)."""


class MessageSchemaError(MessageLoaderError):
    """Raised when a message dict does not conform to expected schema."""


class MessageFileNotFoundError(MessageLoaderError):
    """Raised when the message file cannot be found."""
