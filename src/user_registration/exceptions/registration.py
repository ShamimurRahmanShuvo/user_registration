"""
Registration exception hierarchy foundation.
"""
from __future__ import annotations


class RegistrationError(Exception):
    """Base exception for registration-related errors"""


class UserAlreadyExistsError(RegistrationError):
    """Raised when a username or email is already registered"""


class UserNotFoundError(RegistrationError):
    """Raised when an expected user cannot be found"""
