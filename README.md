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
- Password policy integration
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