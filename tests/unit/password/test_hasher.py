from __future__ import annotations

import pytest

from user_registration.password import Argon2Hasher, PasswordHasher


def test_argon2_hasher_satisfies_protocol() -> None:
    hasher = Argon2Hasher()
    assert isinstance(hasher, PasswordHasher)


def test_hash_returns_string_no_plaintext_password() -> None:
    hasher = Argon2Hasher()
    password = "StrongPassword123!"
    password_hash = hasher.hash(password)

    assert isinstance(password_hash, str)
    assert password_hash
    assert password_hash != password
    assert password not in password_hash


def test_hashes_are_different_for_same_password() -> None:
    hasher = Argon2Hasher()
    password = "StrongPassword123!"
    hash1 = hasher.hash(password)
    hash2 = hasher.hash(password)

    assert hash1 != hash2


def test_verify_password() -> None:
    hasher = Argon2Hasher()
    password = "StrongPassword123!"
    password_hash = hasher.hash(password)

    assert hasher.verify(password, password_hash) is True
    # Wrong Password
    assert hasher.verify("WrongPassword123!", password_hash) is False
    assert hasher.verify("", password_hash) is False


def test_verify_invalid_hash_returns_false() -> None:
    hasher = Argon2Hasher()

    assert hasher.verify("StrongPassword123!", "not-a-valid-password-hash") is False


def test_hash_empty_password_raises_error() -> None:
    hasher = Argon2Hasher()

    with pytest.raises(ValueError, match="Password must not be empty"):
        hasher.hash("")
