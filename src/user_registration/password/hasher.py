"""
Password hashing abstraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError


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


@dataclass(frozen=True, slots=True)
class Argon2Config:
    """
    Argon2 password hashing configuration.
    The defaults coming from argon2-cffi's PasswordHasher
    """

    time_cost: int = 3
    memory_cost: int = 655536
    parallelism: int = 4
    hash_len: int = 32
    salt_len: int = 16

    def __post_init__(self) -> None:
        if self.time_cost < 1:
            raise ValueError("time_cost must be greater than 0")

        if self.memory_cost < 1:
            raise ValueError("memory_cost must be greater than 0")

        if self.parallelism < 1:
            raise ValueError("parallelism must be greater than 0")

        if self.hash_len < 1:
            raise ValueError("hash_len must be greater than 0")

        if self.salt_len < 1:
            raise ValueError("salt_len must be greater than 0")


class Argon2Hasher:
    """
    Argon2id-based password hasher.
    Argon2id is designed specifically for password hashing and provides
    resistance against GPU-based password cracking attacks.
    """

    def __init__(self, config: Argon2Config | None = None) -> None:
        actual_config = config or Argon2Config()
        self._hasher = Argon2PasswordHasher(
            time_cost=actual_config.time_cost,
            memory_cost=actual_config.memory_cost,
            parallelism=actual_config.parallelism,
            hash_len=actual_config.hash_len,
            salt_len=actual_config.salt_len,
        )

    def hash(self, password: str) -> str:
        """
        Hash a plaintext password.
        The returned value contains the Argon2 parameters
        and salt needed for future verification.
        """
        if not password:
            raise ValueError("Password must not be empty")

        return self._hasher.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        """
        Verify a plaintext password against a argon2 hash
        """
        if not password or not password_hash:
            return False

        try:
            return self._hasher.verify(password_hash, password)

        except (VerifyMismatchError, VerificationError, InvalidHashError):
            return False
