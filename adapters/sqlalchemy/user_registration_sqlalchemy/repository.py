from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from user_registration.models import User
from user_registration.repository import DuplicateUserError
from user_registration_sqlalchemy.mapper import to_domain, to_model
from user_registration_sqlalchemy.models import UserModel


class SQLAlchemyUserRepository:
    """
    SQLAlchemy implementation of user repository.
    Transaction ownership remains with the application/service layer.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, user: User) -> User:
        model = to_model(user)

        self._session.add(model)

        try:
            self._session.flush()
        except IntegrityError as exc:
            self._session.rollback()

            raise DuplicateUserError("Username or email is already registered") from exc

        return to_domain(model)

    def get_by_id(self, user_id: UUID) -> User | None:
        model = self._session.get(UserModel, user_id)

        if model is None:
            return None

        return to_domain(model)

    def get_by_username(self, username: str) -> User | None:
        statement = select(UserModel).where(UserModel.username == username)
        model = self._session.scalar(statement)

        if model is None:
            return None

        return to_domain(model)

    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)
        model = self._session.scalar(statement)

        if model is None:
            return None

        return to_domain(model)

    def exists_by_username(self, username: str) -> bool:
        statement = select(UserModel.id).where(UserModel.username == username)

        return self._session.scalar(statement) is not None

    def exists_by_email(self, email: str) -> bool:
        statement = select(UserModel.id).where(UserModel.email == email)

        return self._session.scalar(statement) is not None

    def update(self, user: User) -> User:
        model = self._session.get(UserModel, user.id)

        if model is None:
            raise KeyError(f"User {user.id} does not exist")

        model.username = user.username
        model.email = user.email
        model.password_hash = user.password_hash
        model.updated_at = user.updated_at
        model.is_active = user.is_active

        self._session.flush()

        return to_domain(model)

    def delete(self, user_id: UUID) -> bool:
        model = self._session.get(UserModel, user_id)

        if model is None:
            return False

        self._session.delete(model)
        self._session.flush()

        return True
