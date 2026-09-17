# Architecture

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

## Configuration 

Configuration is represented by:

RegistrationConfig

## Domain Model

Core registration domain object is represented by:

RegistrationRequest

User

# Package boundary

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

```markdown
# Repository Architecture

## Persistence Boundary

The repository layer isolates persistence from the registration domain.

```text
                    Registration Service
                            |
                            v
                    +---------------+
                    | UserRepository|
                    |   Protocol    |
                    +---------------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
         SQLAlchemy      Django       MongoDB
          Adapter        Adapter       Adapter
              |             |             |
              +-------------+-------------+
                            |
                            v
                        Database

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