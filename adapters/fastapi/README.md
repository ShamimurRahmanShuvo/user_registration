# user-registration-fastapi

FastAPI integration for the [`user-registration`](https://pypi.org/project/user-registration/) Python package.

This package provides FastAPI-specific request/response models, dependency integration, and HTTP exception handling while keeping the core registration business logic framework-independent.

## Features

* FastAPI registration endpoint integration
* Pydantic request and response models
* Dependency injection for `RegistrationService`
* HTTP `201 Created` for successful registration
* HTTP `409 Conflict` for duplicate users
* HTTP `422 Unprocessable Entity` for request/validation errors
* HTTP `500 Internal Server Error` for persistence failures
* Compatible with the framework-agnostic `user-registration` package

## Installation

Install the core package and FastAPI adapter:

```bash
pip install user-registration user-registration-fastapi
```

Or install the adapter directly:

```bash
pip install user-registration-fastapi
```

The adapter declares `user-registration` and `fastapi` as dependencies.

## Basic Usage

The adapter exposes a FastAPI router that delegates registration to the core `RegistrationService`.

A typical application structure can look like:

```text
my_app/
├── main.py
├── dependencies.py
└── ...
```

Example:

```python
from fastapi import FastAPI

from user_registration_fastapi import router

app = FastAPI()

app.include_router(router)
```

The registration endpoint is:

```text
POST /users/register
```

Example request:

```json
{
  "username": "shuvo",
  "email": "shuvo@example.com",
  "password": "SecurePassword123!"
}
```

Example successful response:

```json
{
  "id": "...",
  "username": "shuvo",
  "email": "shuvo@example.com"
}
```

The exact response fields depend on the adapter version and configured registration service.

## Dependency Injection

The adapter intentionally does not create a database repository or application-specific `RegistrationService` automatically.

Instead, the application configures the service and provides it through FastAPI dependency injection.

Conceptually:

```python
from fastapi import Depends


def get_registration_service() -> RegistrationService:
    return registration_service
```

The adapter then uses the configured service when handling:

```text
POST /users/register
```

This keeps application infrastructure outside the adapter.

For example:

```text
FastAPI
   │
   ▼
user-registration-fastapi
   │
   ▼
RegistrationService
   │
   ├── PasswordHasher
   ├── PasswordValidator
   ├── UserRepository
   └── ValidationRegistry
```

## HTTP Behavior

The adapter translates domain/application results into HTTP responses.

| Condition                       |                 HTTP Status |
| ------------------------------- | --------------------------: |
| Registration successful         |               `201 Created` |
| Invalid request/validation      |  `422 Unprocessable Entity` |
| Duplicate username/email        |              `409 Conflict` |
| Persistence/application failure | `500 Internal Server Error` |

The adapter does not contain the registration business rules themselves. Those remain in `user-registration`.

## Architecture

The package follows an adapter architecture:

```text
                FastAPI Application
                        │
                        ▼
            user-registration-fastapi
                        │
                        ▼
              RegistrationService
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
        Validation   Password    Repository
         Registry     Hasher      Protocol
                                    │
                                    ▼
                            Application Storage
```

The repository implementation can be supplied by another adapter, such as:

```text
user-registration-sqlalchemy
```

or by an application's own repository implementation.

## Testing

From the repository root:

```bash
.venv/bin/python -m pytest tests/integration/test_fastapi_registration.py -v
```

Run the complete test suite:

```bash
.venv/bin/python -m pytest -v
```

## Development

Install the adapter in editable mode:

```bash
.venv/bin/python -m pip install -e "./adapters/fastapi[dev]"
```

Run Ruff:

```bash
.venv/bin/python -m ruff check adapters/fastapi
```

Check formatting:

```bash
.venv/bin/python -m ruff format --check adapters/fastapi
```

Run MyPy:

```bash
.venv/bin/python -m mypy adapters/fastapi
```

## Compatibility

The adapter requires:

* Python `3.12+`
* FastAPI `>=0.115,<1.0`
* `user-registration >=0.1.0,<1.0.0`

## Related Packages

Core package:

* [`user-registration`](https://pypi.org/project/user-registration/)

SQLAlchemy adapter:

* [`user-registration-sqlalchemy`](https://pypi.org/project/user-registration-sqlalchemy/)

## License

MIT License.

### Visit https://github.com/ShamimurRahmanShuvo/user_registration/tree/main/docs for more detials.
