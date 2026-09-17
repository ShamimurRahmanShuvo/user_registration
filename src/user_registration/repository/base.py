"""
Persistence abstraction.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from user_registration.models import User


@runtime_checkable
class UserRepository(Protocol):
    """
    Persistence contract for User objects.
    Implementations may use any persistence technology, including:
    - SQLAlchemy    - Django ORM    - MongoDB   - DynamoDB      - PostgreSQL
    - MySQL     - SQLite    - in-memory storage     - custom storage systems
    The core user-registration package doesn't depend on any of them
    """
    def create(self, user: User) -> User:
        """
        Persists a new user.
        Args:
            user: User domain object to persist.
        Returns:
            The persisted user.
        """
        ...

    def get_by_id(self, user_id: UUID) -> User | None:
        """
        Retrieve a user by its unique identifier.
        Args:
            user_id: User UUID.
        Returns:
            User if found, otherwise None.
        """
        ...

    def get_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by username.
        Args:
            username: Username to search for.
        Returns:
            User if found, otherwise None.
        """
        ...

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email.
        Args:
            email: Email address to search for.
        Returns:
            User if found, otherwise None.
        """
        ...

    def exists_by_username(self, username: str) -> bool:
        """
        Determine whether a username already exists.
        Args:
            username: Username to check.
        Returns:
            True if the username exists, otherwise False.
        """
        ...

    def exists_by_email(self, email: str) -> bool:
        """
        Determine whether an email already exists.
        Args:
            email: Email address to check.
        Returns:
            True if the email exists, otherwise False.
        """
        ...

    def update(self, user: User) -> User:
        """
        Update an existing user.
        Args:
            user: Updated User domain object.
        Returns:
            The persisted User.
        """
        ...

    def delete(self, user_id: UUID) -> bool:
        """
        Delete a user.
        Args:
            user_id: User UUID.
        Returns:
            True if a user was deleted, otherwise False.
        """
        ...
