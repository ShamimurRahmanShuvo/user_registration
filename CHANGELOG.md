
# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - Phase 4

### Added

- Added `UserRepository` persistence protocol.
- Added repository CRUD contract.
- Added user lookup by UUID.
- Added user lookup by username.
- Added user lookup by email.
- Added username existence check.
- Added email existence check.
- Added repository unit tests using a test-only in-memory implementation.
- Added structural typing tests for repository implementations.

### Design

- Repository abstraction is database-agnostic.
- Repository abstraction is ORM-agnostic.
- Core package does not depend on SQLAlchemy, Django ORM, MongoDB,
  PostgreSQL, MySQL, or other persistence technologies.
- Database implementations will be provided as separate adapters.

## [0.1.0] - Phase 3

### Added

- Added `User` domain model.
- Added `RegistrationRequest` domain input model.
- Added UUID-based user identity.
- Added timezone-aware UTC timestamps.
- Added immutable user state transitions.
- Added active/inactive user state.
- Added password-hash-only representation on `User`.
- Added domain model unit tests.
- Added domain model API documentation.
- Added domain model architecture documentation.

### Design

- Domain models remain framework-agnostic.
- Domain models remain database-agnostic.
- Plaintext passwords are never represented by the `User` model.
- Password hashing remains an infrastructure/service concern.
- Input validation remains separate from domain representation.

## [0.1.0] - Phase 2

### Added

- Added immutable `RegistrationConfig`.
- Added typed registration configuration.
- Added `slots=True` configuration model.
- Added programmatic configuration.
- Added environment-based configuration through `RegistrationConfig.from_env()`.
- Added `USER_REGISTRATION_` environment variable prefix.
- Added integer environment variable parsing.
- Added boolean environment variable parsing.
- Added support for `true/false`, `1/0`, `yes/no`, and `on/off`.
- Added `ConfigurationError`.
- Added username length configuration validation.
- Added configuration unit tests.
- Added configuration API documentation.
- Added configuration architecture documentation.

### Design

- Password policy configuration remains outside `RegistrationConfig`.
- Password policy continues to belong to the `password-validator-s` package.
- `.env` file loading is intentionally not included in the core package.

## [0.1.0] - Phase 1

### Added

- Initial package structure.
- Framework-agnostic architecture.
- Database-agnostic architecture.
- Core package modules.
- Initial testing structure.