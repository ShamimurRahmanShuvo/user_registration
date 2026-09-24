"""
Username validation foundation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UsernameValidator:
    """
    Validates usernames independently from the registration service.
    The validator is configurable so applications can provide different username policy
    """

    min_length: int = 4
    max_length: int = 50
    pattern: str = r"^[a-zA-Z0-9_.-]+$"

    def __post_init__(self) -> None:
        if self.min_length < 1:
            raise ValueError("min_length must be greater than 0")

        if self.max_length < self.min_length:
            raise ValueError("max_length must be greater than or equal to min_length")

    def validate(self, value: str) -> str | None:
        """
        Returns an error message when the username is invalid. None otherwise.
        """
        if len(value) < self.min_length:
            return f"Username must contain atleast {self.min_length} characters"

        if len(value) > self.max_length:
            return f"Username must not be more than {self.max_length} characters"

        if not re.fullmatch(self.pattern, value):
            return "Username contains invalid characters"

        return None
