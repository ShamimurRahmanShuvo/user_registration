from __future__ import annotations

from uuid import UUID, uuid4

from user_registration import User
from user_registration.repository import UserRepository


class InMemoryUserRepository:
    """
    Test implementation of UserRepository.
    This class exists only inside the test suite.
    It demonstrates that an implementation does not need to inherit from
    UserRepository as long as it satisfies the protocol.
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


class IncompleteRepository:
    def create(self, user: User) -> User:
        return user


def create_user(username: str = "test", email: str = "test@example.com") -> User:
    return User.create(
        username=username,
        email=email,
        password_hash="hashed-password",
    )


def test_repository_implementation_satisfies_protocol() -> None:
    repository = InMemoryUserRepository()

    assert isinstance(repository, UserRepository)


def test_create_user() -> None:
    repository = InMemoryUserRepository()
    user = create_user()
    result = repository.create(user)

    assert result == user


def test_get_by_id() -> None:
    repository = InMemoryUserRepository()
    user = create_user()
    repository.create(user)
    result = repository.get_by_id(user.id)

    assert result == user


def test_get_by_id_returns_none_when_user_does_not_exist() -> None:
    repository = InMemoryUserRepository()
    result = repository.get_by_id(uuid4())

    assert result is None


def test_get_by_username() -> None:
    repository = InMemoryUserRepository()
    user = create_user(username="test")
    repository.create(user)
    result = repository.get_by_username("test")

    assert result == user


def test_get_by_username_returns_none_when_user_does_not_exist() -> None:
    repository = InMemoryUserRepository()
    result = repository.get_by_username("unknown")

    assert result is None


def test_get_by_email() -> None:
    repository = InMemoryUserRepository()
    user = create_user(email="test@example.com")
    repository.create(user)
    result = repository.get_by_email("test@example.com")

    assert result == user


def test_get_by_email_returns_none_when_user_does_not_exist() -> None:
    repository = InMemoryUserRepository()
    result = repository.get_by_email("unknown@example.com")

    assert result is None


def test_exists_by_username() -> None:
    repository = InMemoryUserRepository()
    user = create_user(username="test")
    repository.create(user)

    assert repository.exists_by_username("test") is True
    assert repository.exists_by_username("unknown") is False


def test_exists_by_email() -> None:
    repository = InMemoryUserRepository()
    user = create_user(email="test@example.com")
    repository.create(user)

    assert repository.exists_by_email("test@example.com") is True
    assert repository.exists_by_email("unknown@example.com") is False


def test_update_user() -> None:
    repository = InMemoryUserRepository()
    user = create_user(username="test")
    repository.create(user)

    updated_user = User(
        id=user.id,
        username="test-updated",
        email=user.email,
        password_hash=user.password_hash,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active,
    )

    result = repository.update(updated_user)

    assert result == updated_user
    assert repository.get_by_id(user.id) == updated_user


def test_update_nonexistent_user_raises_key_error() -> None:
    repository = InMemoryUserRepository()
    user = create_user()
    try:
        repository.update(user)
    except KeyError as exc:
        assert str(user.id) in str(exc)
    else:
        raise AssertionError("Expected KeyError when updating a nonexistent user")


def test_delete_user() -> None:
    repository = InMemoryUserRepository()
    user = create_user()
    repository.create(user)
    result = repository.delete(user.id)

    assert result is True
    assert repository.get_by_id(user.id) is None


def test_delete_nonexistent_user_returns_false() -> None:
    repository = InMemoryUserRepository()
    result = repository.delete(uuid4())

    assert result is False


def test_repository_methods_have_expected_interface() -> None:
    expected_methods = {
        "create",
        "get_by_id",
        "get_by_username",
        "get_by_email",
        "exists_by_username",
        "exists_by_email",
        "update",
        "delete",
    }

    actual_methods = {name for name in dir(UserRepository) if not name.startswith("_")}

    assert expected_methods.issubset(actual_methods)


def test_incomplete_repository_does_not_satisfy_protocol() -> None:
    repository = IncompleteRepository()

    assert isinstance(repository, UserRepository) is False
