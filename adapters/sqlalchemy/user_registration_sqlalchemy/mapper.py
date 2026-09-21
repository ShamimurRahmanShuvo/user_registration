from __future__ import annotations

from user_registration.models import User

from user_registration_sqlalchemy.models import UserModel


def to_domain(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        email=model.email,
        password_hash=model.password_hash,
        created_at=model.created_at,
        updated_at=model.updated_at,
        is_active=model.is_active
    )


def to_model(user: User) -> UserModel:
    return UserModel(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=user.password_hash,
        created_at=user.created_at,
        updated_at=user.updated_at,
        is_active=user.is_active
    )
