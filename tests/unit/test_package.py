from uuid import UUID

import user_registration
from user_registration import (
    Argon2Config,
    Argon2Hasher,
    ConfigurationError,
    DuplicateUserError,
    EmailValidator,
    FieldValidator,
    NoOpRegistrationHook,
    PasswordHasher,
    PasswordPolicyValidator,
    PasswordValidatorAdapter,
    RegistrationConfig,
    RegistrationError,
    RegistrationHook,
    RegistrationHookError,
    RegistrationPersistenceError,
    RegistrationRequest,
    RegistrationResult,
    RegistrationService,
    RegistrationStatus,
    RepositoryError,
    User,
    UserAlreadyExistsError,
    UsernameValidator,
    UserRepository,
    ValidationError,
    ValidationRegistry,
    create_default_validation_registry,
    generate_token,
)


def test_public_api_exports() -> None:
    expected_exports = {
        "__version__",
        "ConfigurationError",
        "RegistrationConfig",
        "RegistrationRequest",
        "User",
        "UserRepository",
        "RepositoryError",
        "DuplicateUserError",
        "PasswordHasher",
        "Argon2Config",
        "Argon2Hasher",
        "PasswordPolicyValidator",
        "PasswordValidatorAdapter",
        "RegistrationError",
        "UserAlreadyExistsError",
        "RegistrationPersistenceError",
        "RegistrationHookError",
        "RegistrationResult",
        "RegistrationStatus",
        "RegistrationService",
        "RegistrationHook",
        "NoOpRegistrationHook",
        "FieldValidator",
        "ValidationError",
        "UsernameValidator",
        "EmailValidator",
        "ValidationRegistry",
        "create_default_validation_registry",
        "generate_token",
    }

    assert set(user_registration.__all__) == expected_exports


def test_public_api_imports_are_available() -> None:
    public_objects = (
        ConfigurationError,
        RegistrationConfig,
        RegistrationRequest,
        User,
        UserRepository,
        RepositoryError,
        DuplicateUserError,
        PasswordHasher,
        Argon2Config,
        Argon2Hasher,
        PasswordPolicyValidator,
        PasswordValidatorAdapter,
        RegistrationError,
        UserAlreadyExistsError,
        RegistrationPersistenceError,
        RegistrationHookError,
        RegistrationResult,
        RegistrationStatus,
        RegistrationService,
        RegistrationHook,
        NoOpRegistrationHook,
        FieldValidator,
        ValidationError,
        UsernameValidator,
        EmailValidator,
        ValidationRegistry,
        create_default_validation_registry,
        generate_token,
    )

    assert all(obj is not None for obj in public_objects)


def test_package_version_is_defined() -> None:
    assert user_registration.__version__ == "0.1.3"


def test_registration_result_is_public() -> None:
    result = RegistrationResult.successful(UUID(int=1))

    assert result.success is True
    assert result.status is RegistrationStatus.SUCCESS


def test_user_is_public() -> None:
    user = User.create(
        username="test",
        email="test@example.ca",
        password_hash="argon2-hash",
    )

    assert user.username == "test"
