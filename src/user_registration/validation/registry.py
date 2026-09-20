"""
Validator registry foundation.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from user_registration.validation.base import FieldValidator


@dataclass
class ValidationRegistry:
    """
    Registry for field validators.
    Applications can replace or extend validators without modifying RegistrationService
    """
    _validators: dict[str, list[FieldValidator]] = field(default_factory=dict)

    def register(self, field_name: str, validator:FieldValidator) -> None:
        """Register a validator for a field"""
        if not field_name:
            raise ValueError("field_name must not be empty")

        self._validators.setdefault(field_name, []).append(validator)

    def validate(self, field_name: str, value: str) -> list[str]:
        """
        Execute all validators registered for a field.
        Returns validation error message.
        """
        errors: list[str] = []

        for validator in self._validators.get(field_name, []):
            error = validator.validate(value)

            if error is not None:
                errors.append(error)

        return errors

    def has_validators(self, field_name: str) -> bool:
        """Returns whether a validator exists for a field"""

        return bool(self._validators.get(field_name))

    def clear(self, field_name: str) -> None:
        """Remove all validators for a field"""
        self._validators.pop(field_name, None)
