"""
Registration lifecycle hook foundation.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from user_registration.models import User


@runtime_checkable
class RegistrationHook(Protocol):
    """
    Lifecycle extension point for registration.
    Hooks can execute after a user has been successfully persisted.
    """

    def after_registration(self, user: User) -> None:
        """Execute after successful registration"""
        ...


class NoOpRegistrationHook:
    """Default hook that performs no action"""

    def after_registration(self, user: User) -> None:
        return None
