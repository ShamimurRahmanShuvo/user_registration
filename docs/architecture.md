# Architecture

`user-registration` uses dependency inversion and keeps infrastructure outside the core.

```text
Application
    |
    +--> FastAPI adapter (optional)
    |
    +--> SQLAlchemy adapter (optional)
             |
             v
      RegistrationService
       /       |       \
      v        v        v
Validation  Password  UserRepository
Registry    Policy      Protocol
              |
              v
      password-validator-s
```

## Core layers

### Domain

`User` is a framework-independent domain object containing identity, password hash, timestamps, and active state.

### Application service

`RegistrationService` coordinates:

1. Required-field validation
2. Normalization
3. Field validation
4. Duplicate checks
5. Password policy validation
6. Password hashing
7. User creation
8. Persistence
9. Registration hooks
10. Result creation

### Repository

`UserRepository` is a `Protocol`. Implementations can target an in-memory store, SQLAlchemy, PostgreSQL, Django ORM, MongoDB, or another persistence system.

### Password

`PasswordHasher` is a protocol. `Argon2Hasher` is the default implementation.

### Validation

`FieldValidator` and `ValidationRegistry` provide extensible field validation.

## Dependency direction

```text
Adapters / infrastructure
          |
          v
        Core
          |
          v
      Protocols
```

The core must not import FastAPI, SQLAlchemy, Django, or another infrastructure framework.

## Transactions

The application owns transaction boundaries. Repositories flush or persist changes but should not decide the application's overall commit policy.

## Error boundaries

Expected business outcomes use `RegistrationResult`. Repository uniqueness failures use `DuplicateUserError`. Persistence failures can be represented by `RegistrationPersistenceError`. Hook failures use `RegistrationHookError`.
