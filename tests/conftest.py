"""Shared pytest configuration for the project."""

from collections.abc import Iterator
from unittest.mock import Mock

import pytest

from user_registration import (
    Argon2Hasher,
    PasswordValidatorAdapter,
    RegistrationConfig,
    RegistrationService,
    UserRepository,
)


@pytest.fixture
def repository() -> Mock:
    return Mock(spec=UserRepository)


@pytest.fixture
def password_hasher() -> Argon2Hasher:
    return Argon2Hasher()


@pytest.fixture
def password_validator() -> PasswordValidatorAdapter:
    return PasswordValidatorAdapter()


@pytest.fixture
def registration_config() -> RegistrationConfig:
    return RegistrationConfig()


@pytest.fixture
def registration_service(
    repository: Mock,
    password_hasher: Argon2Hasher,
    password_validator: PasswordValidatorAdapter,
    registration_config: RegistrationConfig,
) -> RegistrationService:
    return RegistrationService(
        repository=repository,
        password_hasher=password_hasher,
        password_validator=password_validator,
        config=registration_config,
    )


@pytest.fixture
def cleanup_environment(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    yield
