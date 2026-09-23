"""
Validation abstractions.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class FieldValidator(Protocol):
    """Contract for validating an individual registration field"""

    def validate(self, value: str) -> str | None:
        """Return a validation error or None when the value is valid"""
        ...


class ValidationError:
    """Represents a validation failure"""
