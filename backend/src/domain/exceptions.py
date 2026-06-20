class DomainError(Exception):
    """Base exception for domain errors."""


class ProfileNotFoundError(DomainError):
    """Raised when a profile is not found."""


class InvalidProfileDataError(DomainError):
    """Raised when profile data is invalid."""


class UserNotFoundError(Exception):
    pass
