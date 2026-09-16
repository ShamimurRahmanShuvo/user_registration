# Architecture

## Phase 1
## Architectural Goals

The `user-registration` package is designed to be:

- Framework-agnostic
- Database-agnostic
- Extensible
- Typed
- Testable
- Suitable for production integration
- Independent of application-specific infrastructure

---

# Configuration Architecture

Configuration is represented by:

RegistrationConfig

## Phase 0 package boundary

`user-registration` owns the registration workflow and the contracts required
to validate and persist a user.

It does not own authentication, authorization, sessions, JWTs, OAuth,
password reset, MFA, email delivery, or a specific database/framework.

## Dependency direction

```text
user-registration
    |
    +--> password-validator
    |
    +--> PasswordHasher abstraction
    |
    +--> UserRepository abstraction
```

`password-validator-s` answers whether a password satisfies the configured
password policy. The registration package will separately hash the accepted
password before persistence.

## Planned flow

```text
Registration request
        |
        v
Normalization
        |
        v
Basic field validation
        |
        v
password-validator
        |
        v
Duplicate checks
        |
        v
PasswordHasher.hash()
        |
        v
User domain object
        |
        v
UserRepository.create()
        |
        v
RegistrationResult
```