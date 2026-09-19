from __future__ import annotations

from user_registration import RegistrationRequest, RegistrationService
from user_registration.password import Argon2Hasher, PasswordValidatorAdapter
from tests.fakes.repository import InMemoryUserRepository


def create_service() -> RegistrationService:
    return RegistrationService(
        repository=InMemoryUserRepository(),
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter()
    )


def test_register_valid_user() -> None:
    repository = InMemoryUserRepository()

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter()
    )

    request = RegistrationRequest(
        username="test",
        email="test@example.ca",
        password="StrongPassword123!"
    )

    result = service.register(request)

    assert result.success is True
    assert result.user_id is not None

    user = repository.get_by_id(result.user_id)

    assert user is not None
    assert user.username == "test"
    assert user.email == "test@example.ca"
    assert user.password_hash != "StrongPassword123!"
    assert user.password_hash
    assert "StrongPassword123!" not in user.password_hash


def test_missing_value_is_rejected() -> None:
    service = create_service()

    result = service.register(
        RegistrationRequest(
            username=None,
            email=None,
            password=None
        )
    )

    assert result.success is False
    assert "Username is required" in result.errors
    assert "Email is required" in result.errors
    assert "Password is required" in result.errors


def test_username_and_email_are_normalized() -> None:
    repository = InMemoryUserRepository()

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter()
    )

    result = service.register(
        RegistrationRequest(
            username="  test    ",
            email="  test@example.ca   ",
            password="StrongPassword123!"
        )
    )

    assert result.success is True
    assert result.user_id is not None
    user = repository.get_by_id(result.user_id)
    assert user is not None
    assert user.username == "test"
    assert user.email == "test@example.ca"


def test_duplicate_username_and_email_are_rejected() -> None:
    repository = InMemoryUserRepository()

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter()
    )

    first = service.register(
        RegistrationRequest(
            username="test",
            email="test@example.ca",
            password="StrongPassword123!"
        )
    )
    assert first.success is True

    second = service.register(
        RegistrationRequest(
            username="test",
            email="test@example.ca",
            password="StrongPassword123!"
        )
    )

    assert second.success is False
    assert "Username is already registered" in second.errors
    assert "Email is already registered" in second.errors


def test_duplicate_checks_use_normalized_values() -> None:
    repository = InMemoryUserRepository()

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter(),
    )

    first = service.register(
        RegistrationRequest(
            username="test",
            email="test@example.com",
            password="StrongPassword123!",
        )
    )

    assert first.success is True

    second = service.register(
        RegistrationRequest(
            username=" TEST ",
            email="TEST@EXAMPLE.COM",
            password="StrongPassword123!",
        )
    )

    assert second.success is False
    assert "Username is already registered" in second.errors
    assert "Email is already registered" in second.errors


def test_invalid_email_is_rejected() -> None:
    service = create_service()

    result = service.register(
        RegistrationRequest(
            username="test",
            email="invalid-email",
            password="StrongPassword123!",
        )
    )

    assert result.success is False
    assert "Email address is invalid" in result.errors


def test_short_username_is_rejected() -> None:
    service = create_service()

    result = service.register(
        RegistrationRequest(
            username="ab",
            email="test@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is False
    assert any("Username must contain at least 4 characters" in error for error in result.errors)


def test_long_username_is_rejected() -> None:
    service = create_service()

    result = service.register(
        RegistrationRequest(
            username="a" * 51,
            email="test@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is False
    assert any("at most 50 characters" in error for error in result.errors)


def test_invalid_password_is_rejected() -> None:
    service = create_service()

    result = service.register(
        RegistrationRequest(
            username="test",
            email="test@example.com",
            password="abc",
        )
    )

    assert result.success is False


def test_password_is_hashed_only_after_policy_validation() -> None:
    class TrackingHasher:
        def __init__(self) -> None:
            self.called = False

        def hash(self, password: str) -> str:
            self.called = True
            return "hashed-password"

        def verify(self, password: str, password_hash: str) -> bool:
            return password == password_hash

    repository = InMemoryUserRepository()
    hasher = TrackingHasher()

    service = RegistrationService(
        repository=repository,
        password_hasher=hasher,
        password_validator=PasswordValidatorAdapter(),
    )

    result = service.register(
        RegistrationRequest(
            username="shuvo",
            email="shuvo@example.com",
            password="abc",
        )
    )

    assert result.success is False
    assert hasher.called is False
