from __future__ import annotations

from user_registration import RegistrationConfig, RegistrationRequest, RegistrationService
from user_registration.password import Argon2Hasher, PasswordValidatorAdapter

from tests.fakes.repository import InMemoryUserRepository


def test_custom_username_length_configuration() -> None:
    repository = InMemoryUserRepository()

    config = RegistrationConfig(
        username_min_length=5,
        username_max_length=20,
    )

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter(),
        config=config,
    )

    result = service.register(
        RegistrationRequest(
            username="abcd",
            email="test@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is False
    assert any(
        "at least 5 characters" in error
        for error in result.errors
    )


def test_normalization_can_be_disabled() -> None:
    repository = InMemoryUserRepository()

    config = RegistrationConfig(
        normalize_username=False,
        normalize_email=False,
    )

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter(),
        config=config,
    )

    result = service.register(
        RegistrationRequest(
            username="test",
            email="TEST@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is True
    assert result.user_id is not None

    user = repository.get_by_id(result.user_id)

    assert user is not None
    assert user.username == "test"
    assert user.email == "TEST@example.com"
