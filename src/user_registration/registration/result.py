"""
Registration result foundation.
"""
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegistrationResult:
    """
    Result returned after a registration attempt.
    Successful result contains newly created user's ID
    Failed validation returns errors without exposing sensitive data.
    """
    success: bool
    user_id: UUID | None = None
    errors: tuple[str, ...] = ()

    @classmethod
    def successful(cls, user_id: UUID) -> RegistrationResult:
        return cls(
            success=True,
            user_id=user_id
        )

    @classmethod
    def failed(cls, *errors: str) -> RegistrationResult:
        return cls(
            success=False,
            errors=tuple(errors)
        )
