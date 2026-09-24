# User Registration

A framework-agnostic and database-agnostic user registration package for Python applications.

`user-registration` provides the domain and application layer for registering users while keeping framework and persistence concerns outside the core package.

## Features

- Python 3.12+
- Typed Python API
- Framework independent
- Database independent
- Configurable registration behavior
- Username validation
- Email validation
- Extensible validation registry
- Password policy integration via `password-validator-s`
- Argon2 password hashing
- Repository abstraction
- Custom repository implementations
- Registration hooks
- Duplicate-user detection
- FastAPI adapter
- SQLAlchemy adapter
- Unit and integration tests
- Static type checking with mypy
- Linting and formatting with Ruff

### Core flow

```text
            RegistrationRequest
                 |
                 v
            RegistrationService
 +--------------------------------+
  |      |          |         |
  v      v          v         v
fields validation password repository
                   policy
                     |
                     v
                  hashing
                     |
                     v
                    User
```

## Architecture

The core package does not depend on FastAPI, Django, Flask, SQLAlchemy, PostgreSQL, MongoDB, or any other infrastructure technology.

```text
                       Application
                            |
                            v
                  +--------------------+
                  | RegistrationService|
                  +---------+----------+
                            |
          +-----------------+------------------+
          |                 |                  |
          v                 v                  v
   ValidationRegistry  PasswordHasher   UserRepository
                            |
                            v
                         Argon2
```

### Basic usage

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
        username="shuvo",
        email="shuvo@example.com",
        password="StrongPassword123!",
    )
)

if result.success:
    print(result.user_id)
else:
    print(result.status, result.errors)
```

The application supplies the repository implementation.

### Explicitly out of scope

The core does not implement login, JWT, OAuth/OIDC, sessions, MFA, RBAC, password reset, email delivery, ORM models, database connections, or HTTP routing.

### Development

```bash
.venv/bin/python -m pytest -v
.venv/bin/python -m mypy src
.venv/bin/python -m ruff check src tests
.venv/bin/python -m ruff format --check src tests
.venv/bin/python -m build
```

## License

MIT

### Visit https://github.com/ShamimurRahmanShuvo/user_registration/tree/main/docs, for more details
