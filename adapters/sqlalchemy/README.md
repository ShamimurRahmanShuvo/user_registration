# user-registration-sqlalchemy

SQLAlchemy repository adapter for the [`user-registration`](https://pypi.org/project/user-registration/) Python package.

This package provides a SQLAlchemy 2.x implementation of the repository interfaces required by the framework-agnostic registration service.

It keeps persistence concerns separate from registration business logic.

## Features

* SQLAlchemy 2.x repository implementation
* Implements the `UserRepository` contract from `user-registration`
* Async SQLAlchemy support
* User persistence and lookup
* Username/email duplicate detection
* Database constraint error handling
* Compatible with SQLite, PostgreSQL, MySQL and other SQLAlchemy-supported databases
* Framework independent

## Installation

Install the core package and SQLAlchemy adapter:

```bash
pip install user-registration user-registration-sqlalchemy
```

Or:

```bash
pip install user-registration-sqlalchemy
```

The adapter declares `user-registration` and SQLAlchemy as dependencies.

## Architecture

The adapter implements the repository boundary defined by the core package:

```text
                 RegistrationService
                         │
                         ▼
                 UserRepository
                     Protocol
                         │
                         ▼
          SQLAlchemyUserRepository
                         │
                         ▼
                  SQLAlchemy 2.x
                         │
                         ▼
                     Database
```

The registration service does not need to know whether the application uses SQLite, PostgreSQL, MySQL, or another supported database.

## User Model

The adapter provides a SQLAlchemy user model suitable for persistence.

Conceptually:

```text
User
├── id
├── username
├── email
├── password_hash
└── timestamps / persistence fields
```

Passwords are stored as password hashes rather than plaintext passwords.

Password hashing itself is handled by the core registration package.

## Repository

The primary adapter component is:

```python
SQLAlchemyUserRepository
```

It implements the core repository contract and provides operations required by the registration service, including:

```text
create()
get_by_username()
get_by_email()
exists_by_username()
exists_by_email()
```

The exact available methods are determined by the package version.

## Example

A typical application can compose the components as follows:

```python
from user_registration import RegistrationService
from user_registration_sqlalchemy import SQLAlchemyUserRepository

repository = SQLAlchemyUserRepository(...)

service = RegistrationService(
    repository=repository,
    ...
)
```

The application remains responsible for creating and configuring its SQLAlchemy engine/session infrastructure.

## Database Independence

Because the adapter uses SQLAlchemy, the same repository architecture can support different databases.

For example:

```text
Development
    │
    ▼
SQLite

Testing
    │
    ▼
PostgreSQL

Production
    │
    ▼
PostgreSQL / MySQL / other SQLAlchemy-supported DB
```

The registration service does not need to change when the persistence technology changes.

## Duplicate Users

The adapter translates database uniqueness violations into the core package's duplicate-user domain error.

For example, a unique constraint on:

```text
username
email
```

can be mapped to the registration layer rather than exposing SQLAlchemy-specific exceptions to the application.

This allows the application layer to consistently handle duplicate registration:

```text
Database
   │
   │ IntegrityError
   ▼
SQLAlchemy Adapter
   │
   │ DuplicateUserError
   ▼
RegistrationService
   │
   ▼
Application / API
```

## Transaction Management

The application owns the SQLAlchemy engine/session lifecycle.

The adapter should be integrated into the application's existing transaction management strategy rather than creating an independent application-wide database lifecycle.

This allows applications to control:

* sessions
* transactions
* connection pools
* isolation levels
* database configuration
* migrations

## Testing

Run the SQLAlchemy integration tests from the repository root:

```bash
.venv/bin/python -m pytest tests/integration/test_sqlalchemy_repository.py -v
```

Run all tests:

```bash
.venv/bin/python -m pytest -v
```

## Development

Install the adapter in editable mode:

```bash
.venv/bin/python -m pip install -e "./adapters/sqlalchemy[dev]"
```

Run Ruff:

```bash
.venv/bin/python -m ruff check adapters/sqlalchemy
```

Check formatting:

```bash
.venv/bin/python -m ruff format --check adapters/sqlalchemy
```

Run MyPy:

```bash
.venv/bin/python -m mypy adapters/sqlalchemy
```

## Compatibility

The adapter requires:

* Python `3.12+`
* SQLAlchemy `>=2.0,<3.0`
* `user-registration >=0.1.0,<1.0.0`

## Related Packages

Core package:

* [`user-registration`](https://pypi.org/project/user-registration/)

FastAPI adapter:

* [`user-registration-fastapi`](https://pypi.org/project/user-registration-fastapi/)

## License

MIT License.

### Visit https://github.com/ShamimurRahmanShuvo/user_registration/tree/main/docs for more detials.
