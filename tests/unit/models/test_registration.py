import pytest

from user_registration import RegistrationRequest


def test_registration_request() -> None:
    request = RegistrationRequest(
        username="test",
        email="test@example.com",
        password="StrongPassword123!",
    )

    assert request.username == "test"
    assert request.email == "test@example.com"
    assert request.password == "StrongPassword123!"


def test_registration_request_allows_optional_values() -> None:
    request = RegistrationRequest(
        username=None,
        email=None,
        password=None,
    )

    assert request.username is None
    assert request.email is None
    assert request.password is None


def test_registration_request_is_immutable() -> None:
    request = RegistrationRequest(
        username="test",
        email="test@example.com",
        password="StrongPassword123!",
    )

    with pytest.raises(AttributeError):
        request.username = "another-user"  # type: ignore[misc]


def test_registration_request_uses_slots() -> None:
    request = RegistrationRequest(
        username="test",
        email="test@example.com",
        password="StrongPassword123!",
    )

    assert not hasattr(request, "__dict__")