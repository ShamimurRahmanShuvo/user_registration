from __future__ import annotations

import re
import tomllib
from pathlib import Path
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

ROOT = Path(__file__).resolve().parents[2]


def test_public_api() -> None:
    config = RegistrationConfig()

    assert config is not None
    assert ConfigurationError is not None


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
    assert user_registration.__version__


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


def test_package_version_matches_version_source() -> None:
    version_file = ROOT / "src" / "user_registration" / "_version.py"

    content = version_file.read_text(encoding="utf-8")

    match = re.search(
        r'^__version__\s*=\s*["\']([^"\']+)["\']',
        content,
        re.MULTILINE,
    )

    assert match is not None
    assert user_registration.__version__ == match.group(1)


def _get_source_version(root: Path) -> str:
    version_file = root / "src" / "user_registration" / "_version.py"

    content = version_file.read_text(encoding="utf-8")

    match = re.search(
        r'^__version__\s*=\s*["\']([^"\']+)["\']',
        content,
        re.MULTILINE,
    )

    assert match is not None

    return match.group(1)


def test_all_package_versions_are_synchronized() -> None:
    root = Path(__file__).parents[2]

    source_version = _get_source_version(root)

    adapter_paths = [
        root / "adapters" / "fastapi" / "pyproject.toml",
        root / "adapters" / "sqlalchemy" / "pyproject.toml",
    ]

    for path in adapter_paths:
        with path.open("rb") as file:
            data = tomllib.load(file)

        package_name = data["project"]["name"]
        package_version = data["project"]["version"]

        assert package_version == source_version, (
            f"{package_name} has version {package_version}, "
            f"but source version is {source_version}"
        )
