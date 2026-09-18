from datetime import datetime, timezone
from uuid import UUID

import pytest
from user_registration import User


def test_user_create() -> None:
    user = User.create(
        username="testname",
        email="test@test.ca",
        password_hash="hashed_password"
    )

    assert isinstance(user.id, UUID)
    assert user.username == "testname"
    assert user.email == "test@test.ca"
    assert user.password_hash == "hashed_password"
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
    assert user.created_at.tzinfo == timezone.utc
    assert user.updated_at.tzinfo == timezone.utc
    assert user.is_active is True

    # created and updated time is initially equal
    assert user.created_at == user.updated_at


def test_user_id_is_unique() -> None:
    user1 = User.create(
        username="user1",
        email="user1@test.ca",
        password_hash="hash1"
    )
    user2 = User.create(
        username="user2",
        email="user2@test.ca",
        password_hash="hash2"
    )

    assert user1.id != user2.id


def test_user_is_immutable() -> None:
    user = User.create(
        username="testname",
        email="test@test.ca",
        password_hash="hashed_password"
    )
    with pytest.raises(AttributeError):
        user.username = "new-name"

    # uses slots
    assert not hasattr(user, "__dict__")


def test_user_deactivate() -> None:
    user = User.create(
        username="testname",
        email="test@test.ca",
        password_hash="hashed_password"
    )
    deactivated = user.deactivate()
    assert deactivated.is_active is False
    assert deactivated.id == user.id
    assert deactivated.email == user.email
    assert deactivated.password_hash == user.password_hash
    assert deactivated.created_at == user.created_at
    assert deactivated.updated_at >= user.updated_at


def test_deactivated_does_not_mutate_original_user() -> None:
    user = User.create(
        username="testname",
        email="test@test.ca",
        password_hash="hashed_password"
    )
    deactivate = user.deactivate()
    assert user.is_active is True
    assert deactivate.is_active is False


def test_deactivate_already_inactive_user_returns_same_instance() -> None:
    user = User.create(
        username="testname",
        email="test@test.ca",
        password_hash="hashed_password"
    )
    deactivated = user.deactivate()
    deactivated_again = deactivated.deactivate()
    assert deactivated_again is deactivated


def test_user_activate() -> None:
    user = User.create(
        username="testname",
        email="test@test.ca",
        password_hash="hashed_password"
    )
    inactive_user = user.deactivate()
    active_user = user.activate()

    assert active_user.is_active is True
    assert active_user.id == user.id
    assert active_user.email == user.email
    assert active_user.password_hash == user.password_hash
    assert active_user.created_at == user.created_at
    assert active_user.updated_at >= user.updated_at


def test_activate_already_active_user_returns_same_instance() -> None:
    user = User.create(
        username="testname",
        email="test@test.ca",
        password_hash="hashed_password"
    )
    activated = user.activate()

    assert activated is user


def test_user_stores_password_hash_not_plaintext_password() -> None:
    password_hash = "$argon2id$v=19$example-hash"

    user = User.create(
        username="test",
        email="test@example.com",
        password_hash=password_hash,
    )

    assert user.password_hash == password_hash
    assert not hasattr(user, "password")
