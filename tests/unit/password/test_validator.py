from __future__ import annotations

from password_validator import PasswordValidator
from password_validator.models import ValidationResult

from user_registration.password import PasswordPolicyValidator, PasswordValidatorAdapter


def test_password_validator_adapter_satisfies_protocol() -> None:
    validator = PasswordValidatorAdapter()
    assert isinstance(validator, PasswordPolicyValidator)


def test_validate_returns_validation_result() -> None:
    validator = PasswordValidatorAdapter()
    result = validator.validate("StrongPassword123!")

    assert isinstance(result, ValidationResult)
    assert result.valid is True

    # Invalid Result
    result_invalid = validator.validate("abc")
    assert result_invalid.valid is False


def test_adapter_uses_injected_validator() -> None:
    validator = PasswordValidator()
    adapter = PasswordValidatorAdapter(validator)

    result = adapter.validate("StrongPassword123!")

    assert isinstance(result, ValidationResult)
