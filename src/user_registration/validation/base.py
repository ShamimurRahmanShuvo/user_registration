"""
Validation abstractions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class ValidationError:
    """Represents a validation failure"""
    field: str
    message: str


@runtime_checkable
class FieldValidator(Protocol):
    """Contract for validating an individual registration field"""
    def validate(self, value:str) -> ValidationError | None:
        """Return a validation error or None when the value is valid"""
        ...
