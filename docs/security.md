# Security

## Password Handling

The package never stores plaintext passwords.

Registration passwords are validated and then hashed using Argon2 before
being persisted.

The `User` domain model contains `password_hash`, not the original password.

Applications must never log registration requests or plaintext passwords.

## Password Hashing

The default password hasher is Argon2.

Each password hash receives a unique cryptographic salt.

Applications may provide an `Argon2Config` when they need to tune the
hashing parameters for their environment.

Hashing parameters should be selected based on the application's
performance and security requirements.

## Password Verification

Password verification is delegated to the Argon2 implementation.

A failed verification returns `False` rather than exposing low-level
cryptographic exceptions to callers.

## Security Tokens

Security-sensitive random values are generated using Python's
`secrets` module.

The package must not use `random` for security tokens.

## Sensitive Data

Applications should never log or expose:

- plaintext passwords
- password hashes
- security tokens
- authorization credentials
- database credentials
- connection strings containing credentials

## Registration Errors

Persistence and infrastructure exceptions are translated into
package-level exceptions where appropriate.

Internal exception details should not be exposed through public API
responses.

Applications may log the original exception through exception chaining,
subject to their own logging and security policies.

## Account Enumeration

Registration responses should avoid unnecessarily revealing whether a
specific username or email address exists.

Duplicate registration errors therefore use the generic message:

`Username or email is already registered`

## Transactions

The repository layer does not own the application's outer transaction.

Repositories must not commit or roll back the application's outer
transaction.

Database-specific savepoints may be used to isolate persistence errors.

## Responsibility of the Application

The package provides registration primitives. Applications remain
responsible for:

- HTTPS/TLS
- rate limiting
- CSRF protection where applicable
- abuse prevention
- authentication
- authorization
- session management
- email verification
- MFA
- account lockout policies
- secret management
- security monitoring