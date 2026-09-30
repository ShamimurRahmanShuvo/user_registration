
# Changelog

All notable changes to this project are documented in this file.

The project follows Semantic Versioning.

## 1.0.0rc1 - 2026-09-30

### Added

- Framework-agnostic user registration service.
- Configurable registration validation.
- Password hashing through Argon2.
- Repository protocol for database-agnostic persistence.
- Registration hooks.
- Username and email validation.
- FastAPI adapter.
- SQLAlchemy adapter.
- Registration configuration through environment variables.
- Typed public API.
- Token generation utilities.

### Security

- Passwords are never persisted in plaintext.
- Argon2 password hashing is used for credential storage.
- Duplicate registration responses use generic messaging.
- Persistence errors are wrapped to avoid leaking infrastructure details.
- Token generation uses Python's `secrets` module.
- Registration logging does not include passwords or password hashes.

### Release

- First release candidate for the `1.0.0` stable API.
- Public API frozen for release candidate validation.

## [0.1.3] - 2026-09-25

### Changed

- Improved adapter package quality and Ruff compliance.
- Added adapter documentation.
- Improved package documentation and release documentation.

### Packaging

- Updated core package metadata to `0.1.3`.
- Updated FastAPI adapter to `0.1.3`.
- Updated SQLAlchemy adapter to `0.1.3`.

## [0.1.2]

### Changed

- Internal stabilization changes following the initial alpha releases.

## [0.1.1] - 2026-09-25

### Fixed

- Corrected GitHub Actions package publishing workflow.
- Improved package publishing configuration.

## [0.1.0] - 2026-09-23

Initial alpha release.

### Added

- Framework-independent registration service.
- Database-independent domain model.
- Registration request and result models.
- Environment-based configuration.
- Username validation.
- Email validation.
- Extensible validation registry.
- Password policy integration with `password-validator-s`.
- Argon2 password hashing.
- Password hasher protocol.
- Password validator protocol.
- User repository protocol.
- Repository error abstractions.
- Duplicate-user detection.
- Registration hooks.
- Registration result statuses.
- Security token utility.
- SQLAlchemy adapter.
- FastAPI adapter.
- Unit test suite.
- Integration test suite.
- Strict mypy configuration.
- Ruff configuration.
- Package build configuration.

### Scope

The core package intentionally excludes:

- Login
- Sessions
- JWT
- OAuth/OIDC
- MFA
- RBAC
- Password reset
- Account recovery
- Framework-specific HTTP routing
- ORM-specific persistence logic