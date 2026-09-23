from __future__ import annotations

from tests.fakes import InMemoryUserRepository
from user_registration import (
    Argon2Hasher,
    PasswordValidatorAdapter,
    RegistrationRequest,
    RegistrationService,
    User,
)


class RecordingRegistrationHook:
    def __init__(self) -> None:
        self.users: list[User] = []

    def after_registration(self, user: User) -> None:
        self.users.append(user)


def test_registration_hook_runs_after_successful_registration() -> None:
    repository = InMemoryUserRepository()
    hook = RecordingRegistrationHook()

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter(),
        hooks=(hook,),
    )

    result = service.register(
        RegistrationRequest(
            username="testUser", email="test@example.ca", password="StrongPassword123!"
        )
    )

    assert result.success is True
    assert len(hook.users) == 1
    assert hook.users[0].id == result.user_id


def test_registration_hook_doesnot_run_when_registration_fails() -> None:
    repository = InMemoryUserRepository()
    hook = RecordingRegistrationHook()

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter(),
        hooks=(hook,),
    )

    result = service.register(
        RegistrationRequest(
            username="ab", email="test@example.ca", password="StrongPassword123!"
        )
    )

    assert result.success is False
    assert hook.users == []


def test_multiple_registration_hooks_execute() -> None:
    repository = InMemoryUserRepository()

    first_hook = RecordingRegistrationHook()
    second_hook = RecordingRegistrationHook()

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter(),
        hooks=(
            first_hook,
            second_hook,
        ),
    )

    result = service.register(
        RegistrationRequest(
            username="test",
            email="test@example.com",
            password="StrongPassword123!",
        )
    )

    assert result.success is True

    assert len(first_hook.users) == 1
    assert len(second_hook.users) == 1

    assert first_hook.users[0].id == result.user_id
    assert second_hook.users[0].id == result.user_id
