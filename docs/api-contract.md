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

