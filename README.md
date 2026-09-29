# user-registration

A typed, framework-agnostic, and database-agnostic user registration package for Python applications.

`user-registration` provides the core domain and application services required to register users while keeping HTTP frameworks, databases, ORM implementations, and application infrastructure outside the core package.

## Why user-registration?

The package separates registration business logic from infrastructure.

```text
                    Application
                         |
                         v
              +----------------------+
              | RegistrationService  |
              +----------+-----------+
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
    Validation      Password        Repository
      Registry        Hasher          Protocol
                         |
                         v
                       Argon2
```
The core package does not require FastAPI, Django, Flask, SQLAlchemy, PostgreSQL, MySQL, MongoDB, or another infrastructure technology.

## Features

- Python 3.12+
- Fully typed public API
- Framework independent
- Database independent
- Configurable registration behavior
- Username validation
- Email validation
- Extensible validation registry
- Password policy integration with `password-validator-s`
- Argon2 password hashing
- Repository abstraction
- Duplicate-user detection
- Registration hooks
- Environment-based configuration
- Unit and integration testing
- `mypy` strict type checking
- Ruff linting and formatting

## Packages

The project is distributed as three packages.

| Package                        | Purpose                                               |
| ------------------------------ | ----------------------------------------------------- |
| `user-registration`            | Framework- and database-independent registration core |
| `user-registration-fastapi`    | FastAPI HTTP adapter                                  |
| `user-registration-sqlalchemy` | SQLAlchemy repository adapter                         |

The core package can be used independently of either adapter.

## Installation

### Core package
`pip install user-registration`

### FastAPI Integration
`pip install user-registration-fastapi`

The FastAPI adapter automatically installs the core package and FastAPI.

### SQLAlchemy Integration
`pip install user-registration-sqlalchemy`

The SQLAlchemy adapter automatically installs the core package and SQLAlchemy.

### Full FastAPI + SQLAlchemy stack
`pip install user-registration-fastapi user-registration-sqlalchemy`

## Basic Usage
The core package expects the application to provide a repository implementation.
```python
from user_registration import (
    Argon2Hasher,
    PasswordValidatorAdapter,
    RegistrationConfig,
    RegistrationRequest,
    RegistrationService,
)

service = RegistrationService(
    repository=repository,
    password_hasher=Argon2Hasher(),
    password_validator=PasswordValidatorAdapter(),
    config=RegistrationConfig(),
)

result = service.register(
    RegistrationRequest(
        username="test",
        email="test@example.com",
        password="StrongPassword123!",
    )
)

if result.success:
    print(f"Registered user: {result.user_id}")
else:
    print(result.status)
    print(result.errors)
```
The application supplies the repository implementation.

For example:
```
RegistrationService
       |
       v
UserRepository
       |
       +---- In-memory repository
       +---- SQLAlchemy repository
       +---- PostgreSQL repository
       +---- MongoDB repository
       +---- Custom application repository
```

### Public API
```Python
from user_registration import (
    Argon2Config,
    Argon2Hasher,
    ConfigurationError,
    DuplicateUserError,
    EmailValidator,
    FieldValidator,
    NoOpRegistrationHook,
    PasswordHasher,
    PasswordPolicyValidator,
    PasswordValidatorAdapter,
    RegistrationConfig,
    RegistrationError,
    RegistrationHook,
    RegistrationHookError,
    RegistrationPersistenceError,
    RegistrationRequest,
    RegistrationResult,
    RegistrationService,
    RegistrationStatus,
    User,
    UserAlreadyExistsError,
    UserRepository,
    ValidationError,
    ValidationRegistry,
    UsernameValidator,
    create_default_validation_registry,
    generate_token,
)
```
Applications should prefer these public imports rather than importing internal modules.

### Registration Lifecycle
A registration request follows this general flow:
```commandline
RegistrationRequest
        |
        v
Required-field validation
        |
        v
Normalization
        |
        v
Field validation
        |
        v
Duplicate checks
        |
        v
Password policy validation
        |
        v
Password hashing
        |
        v
User creation
        |
        v
Repository persistence
        |
        v
Registration hooks
        |
        v
RegistrationResult
```

## FastAPI
### Install
`pip install user-registration-fastapi`

Then include the router:
```python
from fastapi import FastAPI

from user_registration_fastapi import router

app = FastAPI()

app.include_router(router)
```
The adapter exposes:

`POST /users/register`

#### Request:
```json
{
  "username": "test",
  "email": "test@example.com",
  "password": "StrongPassword123!"
}
```
#### Successful response:
```json
{
  "user_id": "..."
}
```
#### HTTP Behavior:
| Condition               |                      Status |
| ----------------------- | --------------------------: |
| Successful registration |               `201 Created` |
| Validation failure      |  `422 Unprocessable Entity` |
| Duplicate user          |              `409 Conflict` |
| Persistence failure     | `500 Internal Server Error` |
The application supplies the `RegistrationService` through dependency injection.

See [docs/fastapi.md]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/fastapi.md')

## SQLAlchemy
### Install:
`pip install user-registration-sqlalchemy`

The adapter implements the core repository contract using SQLAlchemy 2.x
```python
from user_registration_sqlalchemy import SQLAlchemyUserRepository

repository = SQLAlchemyUserRepository(session)
```
The application remains responsible for:
- engine configuration
- session lifecycle
- transaction management
- migrations
- database configuration

See [docs/sqlalchemy.md]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/sqlalchemy.md')

## Configuration
Registration behavior can be configured directlyL
```python
from user_registration import RegistrationConfig

config = RegistrationConfig(
    username_min_length=4,
    username_max_length=50,
    email_required=True,
    username_required=True,
    password_required=True,
    normalize_email=True,
    normalize_username=True,
)
```
Environment variables are also supported:
```markdown
USER_REGISTRATION_USERNAME_MIN_LENGTH
USER_REGISTRATION_USERNAME_MAX_LENGTH
USER_REGISTRATION_EMAIL_REQUIRED
USER_REGISTRATION_USERNAME_REQUIRED
USER_REGISTRATION_PASSWORD_REQUIRED
USER_REGISTRATION_NORMALIZE_EMAIL
USER_REGISTRATION_NORMALIZE_USERNAME
```
See [docs/configuration.md]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/configuration.md')

## Password Security
Passwords are validated and hashed using Argon2 before persistence.

The package does not store plaintext passwords.

Security-sensitive tokens use Python's `secrets` module.

Applications should never log plaintext passwords, password hashes,
registration requests containing passwords, or security tokens.

The package intentionally does not implement authentication,
authorization, rate limiting, MFA, or account lockout. Those concerns
belong in the application or authentication layer.

The registration service uses the configured `PasswordHasher` implementation.

The default implementation is based on Argon2:
```python
from user_registration import Argon2Hasher

hasher = Argon2Hasher()

password_hash = hasher.hash("StrongPassword123!")

assert hasher.verify(
    "StrongPassword123!",
    password_hash,
)
```
Password policy validation is provided through the `PasswordPolicyValidator` abstraction.

See [docs/password-security.md]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/password-security.md')

## Extensibility
The package is designed around protocols and dependency injection
### Repository
```python
class UserRepository(Protocol):
    ...
```
Applications can provide their own repository implementation.

### Password hasher
```python
class PasswordHasher(Protocol):
    ...
```
Applications can provide a different password hashing implementation.

### Field validation
Custom validators can be registered:
```python
class ReservedUsernameValidator:
    def validate(self, value: str) -> str | None:
        if value == "admin":
            return "Username is reserved"

        return None
```

See [docs/validation.md]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/validation.md')

### Registration hooks
Applications can register hooks that execute after successful registration

See [docs/hooks.md]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/hooks.md')



## Explicitly out of scope
- Login
- Sessions
- JWT authentication
- 0Auth/OIDC
- MFA
- RBAC
- Password reset
- Account recovery
- Email delivery
- ORM models
- Database connections
- HTTP routing

These concerns belong to the application or separate integration.

## Development
Clone the repository:
```bash
git clone https://github.com/ShamimurRahmanShuvo/user_registration.git
cd user_registration
```
Create a virtual environment:
```bash
python3.14 -m venv .venv
```
Install development dependencies:
```bash
.venv/bin/python -m pip install -e ".[dev]"
```
Run tests:
```bash
.venv/bin/python -m pytest -v
```
Run type checking:
```bash
.venv/bin/python -m mypy src
```
Run linting:
```bash
.venv/bin/python -m ruff check src tests
```
Check formatting:
```bash
.venv/bin/python -m ruff format --check src tests
```
Build the package:
```bash
.venv/bin/python -m build
```
## Documentation
Detailed documentation is available in [docs/]('https://github.com/ShamimurRahmanShuvo/user_registration/tree/main/docs')

- [Architecture]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/architecture.md')
- [API Contract]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/api-contract.md')
- [Configuration]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/configuration.md')
- [Repositories]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/repositories.md')
- [Validation]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/valiidation.md')
- [Password Security]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/password-security.md')
- [Registration Hooks]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/hooks.md')
- [FastAPI Integration]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/fastapi.md')
- [SQLAlchemy Integration]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/sqlalchemy.md')
- [Testing]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/testing.md')
- [Release Guide]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/release.md')

## Versioning
The project follows semantic versioning.

During the `0.x` development series, public APIs may change between minor releases.

The `1.0.0` release will mark the first stable public API contract

See [CHANGELOG.md]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/CHANGELOG.md') for release history.
## License

MIT License

See [LICENSE]('https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/LICENSE')

## Project Links
- [GitHub Repository]('https://github.com/ShamimurRahmanShuvo/user_registration')
- [Issue Tracker]('https://github.com/ShamimurRahmanShuvo/user_registration/issues')
- [Documentation]('https://github.com/ShamimurRahmanShuvo/user_registration/tree/main/docs')
