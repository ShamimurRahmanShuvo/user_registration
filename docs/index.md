# Documentation

## Getting Started

- [Installation](installation.md)
- [Configuration](configuration.md)
- [API Contract](api-contract.md)

## Architecture

- [Architecture](architecture.md)
- [Repositories](repositories.md)
- [Validation](validation.md)
- [Registration Hooks](hooks.md)
- [Password Security](password-security.md)

## Integrations

- [FastAPI](fastapi.md)
- [SQLAlchemy](sqlalchemy.md)
- [Adapters](adapters.md)

## Development

- [Testing](testing.md)
- [Release Guide](release.md)

## Package Structure

```text
user_registration/
├── src/
│   └── user_registration/
│
├── adapters/
│   ├── fastapi/
│   │   └── user_registration_fastapi/
│   │
│   └── sqlalchemy/
│       └── user_registration_sqlalchemy/
│
├── tests/
│   ├── unit/
│   └── integration/
│
└── docs/
```

## Package Responsibilities
### user-registration

Core registration domain and application logic.

### user-registration-fastapi

HTTP/FastAPI integration.

### user-registration-sqlalchemy

SQLAlchemy persistence integration.

The packages intentionally maintain separate responsibilities.