from uuid import uuid4

from user_registration import User
from user_registration.repository import UserRepository


class InMemoryRepository:
    def __init__(self) -> None:
        self.users: dict[object, User] = {}

    def create(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def get_by_id(self, user_id):
        return self.users.get(user_id)

    def get_by_username(self, username: str):
        return next(
            (
                user
                for user in self.users.values()
                if user.username == username
            ),
            None,
        )

    def get_by_email(self, email: str):
        return next(
            (
                user
                for user in self.users.values()
                if user.email == email
            ),
            None,
        )

    def exists_by_username(self, username: str) -> bool:
        return self.get_by_username(username) is not None

    def exists_by_email(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def update(self, user: User) -> User:
        if user.id not in self.users:
            raise KeyError(user.id)

        self.users[user.id] = user
        return user

    def delete(self, user_id) -> bool:
        if user_id not in self.users:
            return False

        del self.users[user_id]
        return True


def test_repository_implements_protocol() -> None:
    repository = InMemoryRepository()

    assert isinstance(repository, UserRepository)


def test_repository_contract() -> None:
    repository = InMemoryRepository()

    user = User.create(
        username="shuvo",
        email="shuvo@example.com",
        password_hash="hash",
    )

    created = repository.create(user)

    assert repository.get_by_id(created.id) == user
    assert repository.get_by_username("shuvo") == user
    assert repository.get_by_email("shuvo@example.com") == user

    assert repository.exists_by_username("shuvo") is True
    assert repository.exists_by_email("shuvo@example.com") is True

    updated = User(
        id=user.id,
        username="updated",
        email=user.email,
        password_hash=user.password_hash,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=False,
    )

    assert repository.update(updated) == updated

    assert repository.delete(user.id) is True
    assert repository.delete(user.id) is False
