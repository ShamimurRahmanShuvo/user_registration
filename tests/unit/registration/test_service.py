from __future__ import annotations

from user_registration.config import RegistrationConfig
from user_registration.models import RegistrationRequest
from user_registration.password import Argon2Hasher, PasswordValidatorAdapter
from user_registration.registration import RegistrationService
from user_registration.validation import (
    ValidationRegistry,
    create_default_validation_registry,
)
from user_registration.repository import DuplicateUserError

from tests.fakes import InMemoryUserRepository


def create_service(
    *,
    config: RegistrationConfig | None = None,
    validation_registry: ValidationRegistry | None = None,
) -> tuple[RegistrationService, InMemoryUserRepository]:
    repository = InMemoryUserRepository()
    actual_config = config or RegistrationConfig()

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter(),
        config=actual_config,
        validation_registry=validation_registry,
    )

    return service, repository


def test_register_valid_user() -> None:
    service, repository = create_service()

    result = service.register(
        RegistrationRequest(
            username="shuvo",
            email="shuvo@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is True
    assert result.user_id is not None

    user = repository.get_by_id(result.user_id)

    assert user is not None
    assert user.username == "shuvo"
    assert user.email == "shuvo@example.com"
    assert user.password_hash != "StrongPassword123!"


def test_username_and_email_are_normalized() -> None:
    service, repository = create_service()

    result = service.register(
        RegistrationRequest(
            username="  Shuvo  ",
            email="  SHUVO@EXAMPLE.COM  ",
            password="StrongPassword123!",
        )
    )

    assert result.success is True
    assert result.user_id is not None

    user = repository.get_by_id(result.user_id)

    assert user is not None
    assert user.username == "shuvo"
    assert user.email == "shuvo@example.com"


def test_duplicate_username_and_email_are_rejected() -> None:
    service, _ = create_service()

    first = service.register(
        RegistrationRequest(
            username="shuvo",
            email="shuvo@example.com",
            password="StrongPassword123!",
        )
    )

    assert first.success is True

    second = service.register(
        RegistrationRequest(
            username="shuvo",
            email="shuvo@example.com",
            password="AnotherStrongPassword123!",
        )
    )

    assert second.success is False
    assert "Username is already registered" in second.errors
    assert "Email is already registered" in second.errors


def test_duplicate_checks_use_normalized_values() -> None:
    service, _ = create_service()

    first = service.register(
        RegistrationRequest(
            username="Shuvo",
            email="Shuvo@Example.com",
            password="StrongPassword123!",
        )
    )

    assert first.success is True

    second = service.register(
        RegistrationRequest(
            username=" shuvo ",
            email=" SHUVO@EXAMPLE.COM ",
            password="AnotherStrongPassword123!",
        )
    )

    assert second.success is False
    assert "Username is already registered" in second.errors
    assert "Email is already registered" in second.errors


def test_invalid_email_is_rejected() -> None:
    service, _ = create_service()

    result = service.register(
        RegistrationRequest(
            username="shuvo",
            email="invalid-email",
            password="StrongPassword123!",
        )
    )

    assert result.success is False
    assert "Email address is invalid" in result.errors


def test_short_username_is_rejected() -> None:
    service, _ = create_service()

    result = service.register(
        RegistrationRequest(
            username="ab",
            email="shuvo@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is False
    assert "Username must contain atleast 4 characters" in result.errors


def test_long_username_is_rejected() -> None:
    service, _ = create_service()

    result = service.register(
        RegistrationRequest(
            username="a" * 51,
            email="shuvo@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is False
    assert "Username must not be more than 50 characters" in result.errors


def test_invalid_password_is_rejected() -> None:
    service, repository = create_service()

    result = service.register(
        RegistrationRequest(
            username="shuvo",
            email="shuvo@example.com",
            password="weak",
        )
    )

    assert result.success is False
    assert repository.get_by_username("shuvo") is None


def test_password_is_hashed_only_after_policy_validation() -> None:
    service, repository = create_service()

    result = service.register(
        RegistrationRequest(
            username="shuvo",
            email="shuvo@example.com",
            password="weak",
        )
    )

    assert result.success is False
    assert repository.get_by_username("shuvo") is None


def test_custom_username_validator_is_supported() -> None:
    class ReservedUsernameValidator:
        def validate(self, value: str) -> str | None:
            if value == "admin":
                return "Username is reserved"
            return None

    config = RegistrationConfig()

    registry = create_default_validation_registry(config)
    registry.register(
        "username",
        ReservedUsernameValidator(),
    )

    service, repository = create_service(
        config=config,
        validation_registry=registry,
    )

    result = service.register(
        RegistrationRequest(
            username="admin",
            email="test@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is False
    assert "Username is reserved" in result.errors
    assert repository.get_by_username("admin") is None


def test_repository_duplicate_error_is_handled() -> None:
    class DuplicateRepository(InMemoryUserRepository):
        def create(self, user):
            raise DuplicateUserError(
                "Database unique constraint violation",
            )

    service = RegistrationService(
        repository=DuplicateRepository(),
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter(),
    )

    result = service.register(
        RegistrationRequest(
            username="test",
            email="test@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is False
    assert result.status.value == "duplicate"
    assert result.user_id is None
