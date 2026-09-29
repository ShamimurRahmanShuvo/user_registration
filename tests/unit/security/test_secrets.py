import pytest

from user_registration.security import generate_token


def test_generate_token_returns_string() -> None:
    token = generate_token()

    assert isinstance(token, str)


def test_generate_token_is_non_empty() -> None:
    token = generate_token()

    assert token
    assert len(token) >= 16


def test_generate_tokens_are_different() -> None:
    first = generate_token()
    second = generate_token()

    assert first != second


def test_token_length_must_meet_minimum() -> None:
    with pytest.raises(ValueError):
        generate_token(15)


def test_generate_token_supports_custom_length() -> None:
    token = generate_token(32)

    assert isinstance(token, str)
    assert len(token) >= 32
