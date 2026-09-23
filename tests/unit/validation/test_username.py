from user_registration.validation import UsernameValidator


def test_validate_username() -> None:
    validator = UsernameValidator()

    assert validator.validate("Test") is None


def test_username_length() -> None:
    validator = UsernameValidator()

    error = validator.validate("ab")
    assert error is not None
    assert "Username must contain atleast 4 characters" in error

    errorLong = validator.validate("a" * 51)
    assert errorLong is not None
    assert "Username must not be more than 50 characters" in errorLong


def test_username_rejects_invalid_characters() -> None:
    validator = UsernameValidator()
    error = validator.validate("test@123")

    assert error == "Username contains invalid characters"


def test_custom_username_limits() -> None:
    validator = UsernameValidator(min_length=5, max_length=10)

    assert validator.validate("testUser") is None
    assert validator.validate("abc") is not None
