"""
Registration request model foundation.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegistrationRequest:
    """
    Input data required to register a user.
    The password is accepted here because it is registration input.
    It must never be persisted directly.
    Password hashing is handled by the password hashing abstraction.
    """

    username: str | None
    email: str | None
    password: str | None
