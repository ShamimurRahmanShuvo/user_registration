# user-registration

A framework-agnostic and extensible Python package for user registration.

The package is designed to provide a reusable registration domain/service layer
without coupling the application to a specific web framework or database.

## Planned responsibilities

- Basic user registration
- Username and email validation
- Password validation through `password-validator-s`
- Secure password hashing
- Repository abstraction for persistence
- Custom registration fields and validators
- Registration lifecycle hooks

## Explicitly out of scope

- Login/authentication
- JWT/session management
- OAuth
- Authorization/RBAC
- Password reset
- MFA
- Email/SMS delivery
- Framework-specific routing
- Database-specific ORM models

## Development

Create a virtual environment and install the project with development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

Run type checking:

```bash
mypy src
```

## Status

Phase 0 and Phase 1: package contract and project foundation.
