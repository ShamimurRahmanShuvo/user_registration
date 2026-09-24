"""
Email validation foundation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmailValidator:
    """Basic framework-independent email validation"""

    require_domain: bool = True

    def validate(self, value: str) -> str | None:
        """Return an error message when the email is invalid. None otherwise"""

        if not value:
            return "Email address is required"

        if "@" not in value:
            return "Email address is invalid"

        local_part, _, domain = value.partition("@")

        if not local_part:
            return "Email address is invalid"

        if self.require_domain and not domain:
            return "Email address is invalid"

        if "." not in domain:
            return "Email address is invalid"

        return None
