# Adapters

Adapters connect the framework-independent core to infrastructure.

Recommended distributions:

```text
user-registration
user-registration-fastapi
user-registration-sqlalchemy
```

## Core

Contains domain models, registration service, validation, hashing abstraction, repository protocol, configuration, hooks, and result types.

## FastAPI

Provides request/response schemas, dependency contract, and the registration router.

```bash
pip install user-registration-fastapi
```

## SQLAlchemy

Provides ORM model, mapping functions, and repository implementation.

```bash
pip install user-registration-sqlalchemy
```

Separating adapters prevents optional framework dependencies from becoming mandatory core dependencies.
