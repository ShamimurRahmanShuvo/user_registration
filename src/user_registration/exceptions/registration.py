"""
Registration exception hierarchy foundation.
"""

from __future__ import annotations


class RegistrationError(Exception):
    """Base exception for registration-related errors"""


class UserAlreadyExistsError(RegistrationError):
    """Raised when a username or email is already registered"""


class RegistrationPersistenceError(RegistrationError):
    """Raised when user persistance fails"""


class RegistrationHookError(RegistrationError):
    """Raised whena registration hook fails"""
