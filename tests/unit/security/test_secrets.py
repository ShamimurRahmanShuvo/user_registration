from user_registration.security import generate_token


def test_generate_token_is_non_empty() -> None:
    token = generate_token()

    assert token
    assert len(token) >= 16


def test_generate_tokens_are_different() -> None:
    first = generate_token()
    second = generate_token()

    assert first != second
