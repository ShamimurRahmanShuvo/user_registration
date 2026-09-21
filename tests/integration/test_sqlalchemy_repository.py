import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from user_registration import User

from user_registration_sqlalchemy import Base, SQLAlchemyUserRepository
from user_registration.repository import DuplicateUserError


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
