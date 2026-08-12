class NexusBIError(Exception):
    """Base exception for expected application errors."""


class AuthenticationError(NexusBIError):
    pass


class AuthorizationError(NexusBIError):
    pass
