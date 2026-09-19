from __future__ import annotations

from uuid import UUID

from user_registration.models import User


class InMemoryUserRepository:
    """
    Test-only repository implementation.

    This class must never be part of the production package.
    """

    def __init__(self) -> None:
        self._users: dict[UUID, User] = {}

    def create(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        return self._users.get(user_id)

    def get_by_username(self, username: str) -> User | None:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def get_by_email(self, email: str) -> User | None:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def exists_by_username(self, username: str) -> bool:
        return self.get_by_username(username) is not None

    def exists_by_email(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def update(self, user: User) -> User:
        if user.id not in self._users:
            raise KeyError(f"User {user.id} does not exist")

        self._users[user.id] = user
        return user

    def delete(self, user_id: UUID) -> bool:
        if user_id not in self._users:
            return False

        del self._users[user_id]
        return True
