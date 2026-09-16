# Public API Contract

The initial public API is intentionally small.

Planned public objects:

- `RegistrationService`
- `RegistrationConfig`
- `RegistrationRequest`
- `RegistrationResult`
- `User`
- `UserRepository`
- `PasswordHasher`

Phase 1 exposes only the package namespace and version. Concrete public
objects will be introduced one phase at a time and covered by tests before
they are considered stable.
