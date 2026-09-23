"""
User domain model foundation.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4


def utc_now() -> datetime:
    """Return the current UTC time as a timezone-aware datetime"""
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class User:
    """
    Domain representation of a registered user.
    This model intentionally contains no ORM or database-specific behaviour.
    Passwords must never be stored in plaintext. Password-hash field contains
    only the result produced by PasswordHasher
    """
    id: UUID
    username: str
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    @classmethod
    def create(cls, *, username: str, email: str, password_hash: str) -> User:
        """
        Create a new user domain object.
        """
        now = utc_now()

        return cls(
            id=uuid4(),
            username=username,
            email=email,
            password_hash=password_hash,
            created_at=now,
            updated_at=now
        )

    def deactivate(self) -> User:
        """
        Return a new user instance marked as inactive.
        """
        if not self.is_active:
            return self

        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            password_hash=self.password_hash,
            created_at=self.created_at,
            updated_at=utc_now(),
            is_active=False
        )

    def activate(self) -> User:
        """
        Return a new user instance marked as active
        """
        if self.is_active:
            return self

        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            password_hash=self.password_hash,
            created_at=self.created_at,
            updated_at=utc_now(),
            is_active=True
        )
