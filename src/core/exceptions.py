"""Custom exceptions for MediaWiki AI Agent."""


class MediaWikiAgentException(Exception):
    """Base exception for the agent."""
    pass


class AuthenticationError(MediaWikiAgentException):
    """Raised when authentication fails."""
    pass


class APIError(MediaWikiAgentException):
    """Raised when API calls fail."""
    pass


class RateLimitError(APIError):
    """Raised when rate limited by MediaWiki."""
    pass


class PageNotFoundError(APIError):
    """Raised when a page is not found."""
    pass


class EditConflictError(APIError):
    """Raised when an edit conflict occurs."""
    pass


class ConfigurationError(MediaWikiAgentException):
    """Raised when configuration is invalid."""
    pass


class IndexingError(MediaWikiAgentException):
    """Raised during indexing operations."""
    pass


class LLMError(MediaWikiAgentException):
    """Raised when LLM operations fail."""
    pass


class ValidationError(MediaWikiAgentException):
    """Raised when data validation fails."""
    pass
