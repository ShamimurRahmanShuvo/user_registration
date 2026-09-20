from user_registration.config import RegistrationConfig
from user_registration.validation import (
    UsernameValidator,
    create_default_validation_registry,
)


def test_default_registry_contains_username_validator() -> None:
    config = RegistrationConfig()

    registry = create_default_validation_registry(config)

    errors = registry.validate("username", "ab")

    assert errors == ["Username must contain atleast 4 characters",]


def test_default_registry_contains_email_validator() -> None:
    config = RegistrationConfig()

    registry = create_default_validation_registry(config)

    errors = registry.validate("email", "invalid")

    assert errors == ["Email address is invalid",]


def test_default_registry_uses_configured_username_limits() -> None:
    config = RegistrationConfig(
        username_min_length=5,
        username_max_length=10,
    )

    registry = create_default_validation_registry(config)

    errors = registry.validate("username", "abcd")

    assert errors == ["Username must contain atleast 5 characters",]