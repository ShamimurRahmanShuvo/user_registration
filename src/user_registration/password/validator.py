from __future__ import annotations
from typing import Protocol, runtime_checkable


@runtime_checkable
class PasswordValidator(Protocol):
    """
    Contract for password policy validation.
    This abstraction intentionally does not know how passwords are hashed or persisted.
    """
    def validate(self, password: str) -> bool:
        """
        Return True when the password satisfies the configured policy
        """
        ...
