"""
Registration result foundation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class RegistrationStatus(StrEnum):
    SUCCESS = "success"
    VALIDATION_ERROR = "validation_error"
    DUPLICATE = "duplicate"
    PERSISTENCE_ERROR = "persistence_error"


@dataclass(frozen=True, slots=True)
class RegistrationResult:
    """
    Result returned after a registration attempt.
    Successful result contains newly created user's ID
    Failed validation returns errors without exposing sensitive data.
    """

    success: bool
    status: RegistrationStatus
    user_id: UUID | None = None
    errors: tuple[str, ...] = ()

    @classmethod
    def successful(cls, user_id: UUID) -> RegistrationResult:
        return cls(success=True, user_id=user_id, status=RegistrationStatus.SUCCESS)

    @classmethod
    def validation_failed(cls, *errors: str) -> RegistrationResult:
        return cls(
            success=False,
            errors=tuple(errors),
            status=RegistrationStatus.VALIDATION_ERROR,
        )

    @classmethod
    def duplicate(cls, *errors: str) -> RegistrationResult:
        return cls(
            success=False,
            status=RegistrationStatus.DUPLICATE,
            errors=tuple(errors),
        )

    @classmethod
    def persistence_failed(cls, *errors: str) -> RegistrationResult:
        return cls(
            success=False,
            status=RegistrationStatus.PERSISTENCE_ERROR,
            errors=tuple(errors),
        )
