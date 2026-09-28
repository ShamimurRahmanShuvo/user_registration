import pytest

from user_registration.validation import UsernameValidator, ValidationRegistry


class ReservedUsernameValidator:
    def validate(self, value: str) -> str | None:
        if value == "admin":
            return "Username is reserved"

        return None


class MinimumUsernameValidator:
    def __init__(self, minimum: int) -> None:
        self.minimum = minimum

    def validate(self, value: str) -> str | None:
        if len(value) < self.minimum:
            return f"Username must contain at least {self.minimum} characters"

        return None


def test_registry_registers_validator() -> None:
    registry = ValidationRegistry()

    registry.register("username", UsernameValidator())
    assert registry.has_validators("username") is True


def test_registry_validates_field() -> None:
    registry = ValidationRegistry()

    registry.register("username", UsernameValidator())

    errors = registry.validate("username", "ab")

    assert errors == ["Username must contain atleast 4 characters"]


def test_registry_supports_multiple_validators() -> None:
    registry = ValidationRegistry()

    registry.register("username", UsernameValidator())

    registry.register("username", ReservedUsernameValidator())

    errors = registry.validate("username", "admin")

    assert errors == ["Username is reserved"]


def test_registry_returns_multiple_errors() -> None:
    registry = ValidationRegistry()

    registry.register("username", UsernameValidator(min_length=10))

    registry.register("username", ReservedUsernameValidator())

    errors = registry.validate("username", "admin")

    assert len(errors) == 2
    assert errors == [
        "Username must contain atleast 10 characters",
        "Username is reserved",
    ]


def test_registry_clear() -> None:
    registry = ValidationRegistry()

    registry.register("username", UsernameValidator())

    registry.clear("username")

    assert registry.has_validators("username") is False


def test_register_normalizes_field_name() -> None:
    class Validator:
        def validate(self, value: str) -> str | None:
            return "Invalid"

    registry = ValidationRegistry()
    registry.register("USERNAME", Validator())

    assert registry.has_validators("username")
    assert registry.has_validators("USERNAME")

    errors = registry.validate("username", "test")
    assert errors == ["Invalid"]


def test_register_rejects_empty_field_name() -> None:
    class Validator:
        def validate(self, value: str) -> str | None:
            return None

    registry = ValidationRegistry()

    with pytest.raises(ValueError, match="field_name must not be empty"):
        registry.register("   ", Validator())
