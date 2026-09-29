from datetime import UTC, datetime
from uuid import uuid4

from user_registration_sqlalchemy import UserModel, to_domain, to_model

from user_registration import User


def test_to_model() -> None:
    now = datetime.now(UTC)

    user = User(
        id=uuid4(),
        username="test",
        email="test@example.com",
        password_hash="argon2-hash",
        created_at=now,
        updated_at=now,
        is_active=True,
    )

    model = to_model(user)

    assert isinstance(model, UserModel)
    assert model.id == user.id
    assert model.username == user.username
    assert model.email == user.email
    assert model.password_hash == user.password_hash
    assert model.created_at == user.created_at
    assert model.updated_at == user.updated_at
    assert model.is_active == user.is_active


def test_to_domain() -> None:
    now = datetime.now(UTC)
    user_id = uuid4()

    model = UserModel(
        id=user_id,
        username="test",
        email="test@example.com",
        password_hash="argon2-hash",
        created_at=now,
        updated_at=now,
        is_active=True,
    )

    user = to_domain(model)

    assert isinstance(user, User)
    assert user.id == user_id
    assert user.username == "test"
    assert user.email == "test@example.com"
    assert user.password_hash == "argon2-hash"
    assert user.created_at == now
    assert user.updated_at == now
    assert user.is_active is True
