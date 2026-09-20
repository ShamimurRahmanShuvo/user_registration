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

    def register(self, field_name: str, validator: FieldValidator) -> None:
        """Register a validator for a field"""
        normalized_field_name = field_name.strip().lower()

        if not normalized_field_name:
            raise ValueError("field_name must not be empty")

        self._validators.setdefault(field_name, []).append(validator)

    def validate(self, field_name: str, value: str) -> list[str]:
        """
        Execute all validators registered for a field.
        Returns validation error message.
        """
        normalized_field_name = field_name.strip().lower()
        errors: list[str] = []

        for validator in self._validators.get(normalized_field_name, []):
            error = validator.validate(value)

            if error is not None:
                errors.append(error)

        return errors

    def has_validators(self, field_name: str) -> bool:
        """Returns whether a validator exists for a field"""
        normalized_field_name = field_name.strip().lower()

        return bool(self._validators.get(normalized_field_name))

    def clear(self, field_name: str) -> None:
        """Remove all validators for a field"""
        normalized_field_name = field_name.strip().lower()

        self._validators.pop(normalized_field_name, None)

    def clear_all(self) -> None:
        self._validators.clear()
