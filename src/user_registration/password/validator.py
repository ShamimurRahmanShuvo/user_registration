from __future__ import annotations
from typing import Protocol, runtime_checkable
from password_validator import PasswordValidator
from password_validator.models import ValidationResult


@runtime_checkable
class PasswordPolicyValidator(Protocol):
    """
    Contract for password policy validation.
    This abstraction intentionally does not know how passwords are hashed or persisted.
    """
    def validate(self, password: str) -> object:
        """
        Return True when the password satisfies the configured policy
        """
        ...


class PasswordValidatorAdapter:
    """
    Adapter around the password-validator-s package.
    The adapter prevents the rest of user-registration from being tightly
    coupled to the third-party password validation implementation.
    """
    def __init__(self, validator: PasswordValidator | None = None) -> None:
        self._validator = validator or PasswordValidator()

    def validate(self, password: str) -> ValidationResult:
        result = self._validator.validate(password)
        return result
