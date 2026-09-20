from uuid import uuid4

from user_registration.registration import (
    RegistrationResult,
    RegistrationStatus,
)


def test_successful_registration_result() -> None:
    user_id = uuid4()

    result = RegistrationResult.successful(user_id)

    assert result.success is True
    assert result.status is RegistrationStatus.SUCCESS
    assert result.user_id == user_id
    assert result.errors == ()


def test_validation_failure_result() -> None:
    result = RegistrationResult.validation_failed(
        "Username is invalid",
    )

    assert result.success is False
    assert result.status is RegistrationStatus.VALIDATION_ERROR
    assert result.user_id is None
    assert result.errors == ("Username is invalid",)


def test_duplicate_result() -> None:
    result = RegistrationResult.duplicate(
        "Username is already registered",
    )

    assert result.success is False
    assert result.status is RegistrationStatus.DUPLICATE


def test_persistence_failure_result() -> None:
    result = RegistrationResult.persistence_failed(
        "Unable to persist registered user",
    )

    assert result.success is False
    assert result.status is RegistrationStatus.PERSISTENCE_ERROR
