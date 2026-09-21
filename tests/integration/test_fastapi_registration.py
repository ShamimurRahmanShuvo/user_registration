from fastapi import FastAPI
from fastapi.testclient import TestClient

from user_registration import (
    Argon2Hasher,
    PasswordValidatorAdapter,
    RegistrationConfig,
    RegistrationService,
)

from user_registration_fastapi import get_registration_service, router

from tests.fakes import InMemoryUserRepository


def create_app() -> FastAPI:
    app = FastAPI()

    repository = InMemoryUserRepository()

    service = RegistrationService(
        repository=repository,
        password_hasher=Argon2Hasher(),
        password_validator=PasswordValidatorAdapter(),
        config=RegistrationConfig(),
    )

    def override_service() -> RegistrationService:
        return service

    app.dependency_overrides[
        get_registration_service
    ] = override_service

    app.include_router(router)

    return app


def test_register_user() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.post(
        "/users/register",
        json={
            "username": "test",
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert "user_id" in body


def test_duplicate_user_returns_conflict() -> None:
    app = create_app()

    client = TestClient(app)

    payload = {
        "username": "test",
        "email": "test@example.com",
        "password": "StrongPassword123!",
    }

    first = client.post(
        "/users/register",
        json=payload,
    )

    assert first.status_code == 201

    second = client.post(
        "/users/register",
        json=payload,
    )

    assert second.status_code == 409


def test_invalid_username_returns_validation_error() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.post(
        "/users/register",
        json={
            "username": "ab",
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 422

    body = response.json()

    assert "Username must contain atleast 4 characters" in (
        body["detail"]
    )


def test_invalid_email_returns_unprocessable_entity() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == [
        "Email address is invalid",
    ]


def test_duplicate_email_returns_conflict() -> None:
    app = create_app()

    client = TestClient(app)

    first = client.post(
        "/users/register",
        json={
            "username": "firstuser",
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert first.status_code == 201

    second = client.post(
        "/users/register",
        json={
            "username": "seconduser",
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert second.status_code == 409
    assert second.json()["detail"] == [
        "Email is already registered",
    ]


def test_missing_username_returns_422() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 422


def test_missing_email_returns_422() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 422


def test_missing_password_returns_422() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
        },
    )

    assert response.status_code == 422


def test_successful_registration_does_not_return_password() -> None:
    app = create_app()

    client = TestClient(app)

    password = "StrongPassword123!"

    response = client.post(
        "/users/register",
        json={
            "username": "secureuser",
            "email": "secure@example.com",
            "password": password,
        },
    )

    assert response.status_code == 201

    response_body = response.json()

    assert "password" not in response_body
    assert "password_hash" not in response_body
    assert password not in response.text


from uuid import UUID


def test_successful_registration_returns_user_id() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert "user_id" in body
    UUID(body["user_id"])


def test_extra_fields_are_rejected() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123!",
            "is_admin": True,
        },
    )

    assert response.status_code == 422


def test_weak_password_returns_unprocessable_entity() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "abc",
        },
    )

    assert response.status_code == 422
