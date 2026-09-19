from __future__ import annotations

from collections.abc import Generator

import pytest

from user_registration.password import Argon2Hasher, PasswordValidatorAdapter
from user_registration.repository import UserRepository


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users = {}

    def create(self, user):
        self._users[user.id] = user
        return user

    def get_by_id(self, user_id):
        return self._users.get(user_id)

    def get_by_username(self, username):
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def get_by_email(self, email):
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def exists_by_username(self, username):
        return self.get_by_username(username) is not None

    def exists_by_email(self, email):
        return self.get_by_email(email) is not None

    def update(self, user):
        self._users[user.id] = user
        return user

    def delete(self, user_id):
        if user_id not in self._users:
            return False

        del self._users[user_id]
        return True


@pytest.fixture
def repository() -> Generator[UserRepository, None, None]:
    yield InMemoryUserRepository


@pytest.fixture
def password_hasher() -> Argon2Hasher:
    return Argon2Hasher()


@pytest.fixture
def password_validator() -> PasswordValidatorAdapter:
    return PasswordValidatorAdapter()
