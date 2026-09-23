from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from user_registration_sqlalchemy import Base, SQLAlchemyUserRepository

from user_registration import User
from user_registration.repository import DuplicateUserError


@pytest.fixture
def session() -> Session:
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def repository(session: Session) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)


@pytest.fixture
def user() -> User:
    now = datetime.now(UTC)

    return User(
        id=uuid4(),
        username="testuser",
        email="test@example.ca",
        password_hash="$argon2id$v=19$test-hash",
        created_at=now,
        updated_at=now,
        is_active=True
    )


def test_create_and_get_user(repository: SQLAlchemyUserRepository, user: User) -> None:
    created = repository.create(user)

    assert created.id == user.id
    assert created.username == user.username
    assert created.email == user.email
    assert created.password_hash == user.password_hash
    assert created.is_active is True

    # By id
    found = repository.get_by_id(user.id)
    assert found is not None
    assert found.id == user.id
    assert found.username == user.username
    assert found.email == user.email

    # By username
    found_user = repository.get_by_username("testuser")
    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.username == "testuser"

    # By email
    found_email = repository.get_by_email("test@example.ca")
    assert found_email is not None
    assert found_email.id == user.id
    assert found_email.email == "test@example.ca"


def test_get_behavior_when_missing(repository: SQLAlchemyUserRepository) -> None:
    result = repository.get_by_username("non-existent")
    assert result is None

    result_email = repository.get_by_email("missing@example.ca")
    assert result_email is None

    result_id = repository.get_by_id(uuid4())
    assert result_id is None


def test_exists_behaviour(repository: SQLAlchemyUserRepository, user: User) -> None:
    assert repository.exists_by_username("testuser") is False
    assert repository.exists_by_email("test@example.ca") is False

    repository.create(user)

    assert repository.exists_by_username("testuser") is True
    assert repository.exists_by_email("test@example.ca") is True


def test_update_user(repository: SQLAlchemyUserRepository, user: User) -> None:
    repository.create(user)

    updated = User(
        id=user.id,
        username="updateduser",
        email="updated@example.com",
        password_hash="updated-hash",
        created_at=user.created_at,
        updated_at=datetime.now(UTC),
        is_active=False,
    )

    result = repository.update(updated)

    assert result.id == user.id
    assert result.username == "updateduser"
    assert result.email == "updated@example.com"
    assert result.password_hash == "updated-hash"
    assert result.is_active is False

    found = repository.get_by_id(user.id)

    assert found is not None
    assert found.username == "updateduser"
    assert found.email == "updated@example.com"
    assert found.password_hash == "updated-hash"
    assert found.is_active is False


def test_update_missing_user_raises_key_error(
        repository: SQLAlchemyUserRepository
) -> None:
    user = User.create(
        username="missing",
        email="missing@example.com",
        password_hash="hash",
    )

    with pytest.raises(KeyError):
        repository.update(user)


def test_delete_user(repository: SQLAlchemyUserRepository, user: User) -> None:
    repository.create(user)

    deleted = repository.delete(user.id)
    assert deleted is True
    assert repository.get_by_id(user.id) is None


def test_delete_missing_user_returns_false(
        repository: SQLAlchemyUserRepository
) -> None:
    deleted = repository.delete(uuid4())

    assert deleted is False


def test_duplicate_username_and_email_raises_duplicate_user_error(
        repository: SQLAlchemyUserRepository, user: User
) -> None:
    repository.create(user)

    duplicate = User(
        id=uuid4(),
        username=user.username,
        email="different@example.com",
        password_hash="different-hash",
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=True,
    )

    with pytest.raises(DuplicateUserError):
        repository.create(duplicate)

    # Duplicate email
    repository.create(user)
    duplicate_email = User(
        id=uuid4(),
        username="differentuser",
        email=user.email,
        password_hash="different-hash",
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=True,
    )

    with pytest.raises(DuplicateUserError):
        repository.create(duplicate_email)


def test_sqlalchemy_repository_persists_user() -> None:
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = SQLAlchemyUserRepository(
            session,
        )

        user = User.create(
            username="test",
            email="test@example.com",
            password_hash="argon2-hash",
        )

        persisted = repository.create(user)

        session.commit()

        loaded = repository.get_by_id(persisted.id)

        assert loaded is not None
        assert loaded.id == user.id
        assert loaded.username == "test"
        assert loaded.email == "test@example.com"


def test_sqlalchemy_repository_rejects_duplicate_username() -> None:
    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = SQLAlchemyUserRepository(
            session,
        )

        first = User.create(
            username="test",
            email="one@example.com",
            password_hash="hash",
        )

        second = User.create(
            username="test",
            email="two@example.com",
            password_hash="hash",
        )

        repository.create(first)
        session.commit()

        with pytest.raises(DuplicateUserError):
            repository.create(second)


def test_repository_persists_password_hash(
    repository: SQLAlchemyUserRepository,
) -> None:
    user = User.create(
        username="securityuser",
        email="security@example.com",
        password_hash="$argon2id$v=19$example-hash",
    )

    repository.create(user)

    stored = repository.get_by_id(user.id)

    assert stored is not None
    assert stored.password_hash == "$argon2id$v=19$example-hash"
