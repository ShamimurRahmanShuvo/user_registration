from __future__ import annotations

from user_registration.password import PasswordValidator


class FakePasswordValidator:
    def validate(self, password: str) -> bool:
        return len(password) >= 8


def test_password_validator_protocol() -> None:
    validator = FakePasswordValidator()

    assert isinstance(validator, PasswordValidator)


def test_password_validator_accepts_valid_password() -> None:
    validator = FakePasswordValidator()

    assert validator.validate("Strong123!") is True


def test_password_validator_rejects_short_password() -> None:
    validator = FakePasswordValidator()

    assert validator.validate("short") is False


class IncompletePasswordValidator:
    def something_else(self, password: str) -> bool:
        return True


def test_incomplete_password_validator_does_not_satisfy_protocol() -> None:
    validator = IncompletePasswordValidator()

    assert isinstance(validator, PasswordValidator) is False
