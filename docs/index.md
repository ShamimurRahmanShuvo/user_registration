# Documentation

## Getting Started

- [Installation](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/installation.md)
- [Configuration](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/configuration.md)
- [API Contract](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/api-contract.md)

## Architecture

- [Architecture](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/architecture.md)
- [Repositories](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/repositories.md)
- [Validation](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/validation.md)
- [Registration Hooks](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/hooks.md)
- [Password Security](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/password-security.md)

## Integrations

- [FastAPI](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/fastapi.md)
- [SQLAlchemy](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/sqlalchemy.md)
- [Adapters](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/adapters.md)

## Development

- [Testing](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/testing.md)
- [Release Guide](https://github.com/ShamimurRahmanShuvo/user_registration/blob/main/docs/release.md)

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