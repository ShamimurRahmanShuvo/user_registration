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
