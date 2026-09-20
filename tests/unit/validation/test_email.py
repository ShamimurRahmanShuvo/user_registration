from user_registration.validation import EmailValidator


def test_valid_email() -> None:
    validator = EmailValidator()

    assert validator.validate("test@example.ca") is None


def test_email_without_at_symbol_is_invalid() -> None:
    validator = EmailValidator()

    assert validator.validate("testexample.ca") == "Email address is invalid"


def test_email_without_local_part_is_invalid() -> None:
    validator = EmailValidator()

    assert validator.validate("@example.ca") == "Email address is invalid"


def test_email_without_domain_is_invalid() -> None:
    validator = EmailValidator()

    assert validator.validate("test@") == "Email address is invalid"


def test_email_without_domain_dot_is_invalid() -> None:
    validator = EmailValidator()

    assert validator.validate("test@example") == "Email address is invalid"
