"""
Password hashing abstraction.
"""
from __future__ import annotations
from typing import Protocol, runtime_checkable

from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2.exception import InvalidHashError, VerificationError, VerifyMatchError


@runtime_checkable
class PasswordHasher(Protocol):
    """
    Abstraction for securely hashing and verifying passwords.
    Implementations must never expose or persist plaintext passwords.
    """
    def hash(self, password: str) -> str:
        """
        Return a secure password hash for the supplied plaintext password.
        """
        ...

    def verify(self, password: str, password_hash: str) -> bool:
        """
        Verify a plaintext password against a stored password hash
        """
        ...


class Argon2Hasher:
    """
    Argon2id-based password hasher.
    Argon2id is designed specifically for password hashing and provides resistance against GPU-based password
    cracking attacks.
    """
    def __init__(self) -> None:
        self._hasher = Argon2PasswordHasher()

    def hash(self, password: str) -> str:
        """
        Hash a plaintext password.
        The returned value contains the Argon2 parameters and salt needed for future verification.
        """
        if not password:
            raise ValueError("Password must not be empty")

        return self._hasher.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        """
        Verify a plaintext password against a argon2 hash
        """
        if not password:
            return False

        if not password_hash:
            return False

        try:
            return self._hasher.verify(password_hash, password)
        except (VerifyMatchError, VerificationError, InvalidHashError):
            return False
