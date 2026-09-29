# API Contract

## Overview

`user-registration` provides a framework-agnostic user registration
workflow for Python applications' registration workflow.

The package does not depend on:

- Web framework
- Database
- ORM
- Authentication system
- API framework

Framework and database integrations are implemented outside the core package.

---

## Repository Transaction Contract

The `UserRepository` is transaction-aware but does not own the application's
outer transaction.

Repository implementations:

- must not commit the caller's transaction
- must not roll back the caller's transaction
- may use savepoints to isolate operation-level failures
- must translate persistence-specific duplicate errors to
  `DuplicateUserError`

The SQLAlchemy adapter follows this contract using nested transactions.

## Concurrency and Uniqueness

The registration service performs pre-persistence duplicate checks:

```text
exists_by_username
exists_by_email
```

These checks are not sufficient for concurrency safety.

The persistence layer must also enforce unique constraints.

Therefore the expected behavior is:
```text
Request A ----\
               +--> existence check
Request B ----/

Both may see "not found"

        |
        v

Database unique constraint
        |
        +--> one succeeds
        |
        +--> one receives DuplicateUserError
```
The database constraint is the final authority.

## Public API Contract

### Core Package

The following imports are part of the supported public API:

```python
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
    RepositoryError,
    User,
    UserAlreadyExistsError,
    UserRepository,
    UsernameValidator,
    ValidationError,
    ValidationRegistry,
    create_default_validation_registry,
    generate_token,
)
```

# API Contract

## RegistrationRequest

```python
@dataclass(frozen=True, slots=True)
class RegistrationRequest:
    username: str | None
    email: str | None
    password: str | None
```

The password is input only and must never be persisted directly.

## User

```python
@dataclass(frozen=True, slots=True)
class User:
    id: UUID
    username: str
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
```

## RegistrationResult

```python
class RegistrationStatus(StrEnum):
    SUCCESS = "success"
    VALIDATION_ERROR = "validation_error"
    DUPLICATE = "duplicate"
    PERSISTENCE_ERROR = "persistence_error"
```

```python
@dataclass(frozen=True, slots=True)
class RegistrationResult:
    success: bool
    user_id: UUID | None = None
    errors: tuple[str, ...] = ()
    status: RegistrationStatus = RegistrationStatus.SUCCESS
```

Factories:

```python
RegistrationResult.successful(user_id)
RegistrationResult.validation_failed(...)
RegistrationResult.duplicate(...)
RegistrationResult.persistence_failed(...)
```

The `success` field remains for backward compatibility.

## UserRepository

```python
class UserRepository(Protocol):
    def create(self, user: User) -> User: ...
    def get_by_id(self, user_id: UUID) -> User | None: ...
    def get_by_username(self, username: str) -> User | None: ...
    def get_by_email(self, email: str) -> User | None: ...
    def exists_by_username(self, username: str) -> bool: ...
    def exists_by_email(self, email: str) -> bool: ...
    def update(self, user: User) -> User: ...
    def delete(self, user_id: UUID) -> bool: ...
```

## PasswordHasher

```python
class PasswordHasher(Protocol):
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, password_hash: str) -> bool: ...
```

## PasswordPolicyValidator

```python
class PasswordPolicyValidator(Protocol):
    def validate(self, password: str) -> ValidationResult: ...
```

## FieldValidator

```python
class FieldValidator(Protocol):
    def validate(self, value: str) -> str | None: ...
```

`None` means valid.

## RegistrationHook

```python
class RegistrationHook(Protocol):
    def after_registration(self, user: User) -> None: ...
```

## Standard duplicate errors

```text
Username is already registered
Email is already registered
```

## FastAPI mapping

| Status | HTTP |
|---|---:|
| SUCCESS | 201 |
| VALIDATION_ERROR | 422 |
| DUPLICATE | 409 |
| PERSISTENCE_ERROR | 500 |

