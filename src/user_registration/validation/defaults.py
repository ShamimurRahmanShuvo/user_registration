from __future__ import annotations

from user_registration.config import RegistrationConfig
from user_registration.validation.email import EmailValidator
from user_registration.validation.registry import ValidationRegistry
from user_registration.validation.username import UsernameValidator


def create_default_validation_registry(config: RegistrationConfig) -> ValidationRegistry:
    """
    Create the default validation registry for the package.

    Applications can create this registry and add custom validators
    before passing it to RegistrationService.
    """

    registry = ValidationRegistry()

    if config.username_required:
        registry.register(
            "username",
            UsernameValidator(
                min_length=config.username_min_length,
                max_length=config.username_max_length,
            ),
        )

    if config.email_required:
        registry.register("email", EmailValidator())

    return registry
