
# Changelog

All notable changes to this project are documented in this file.

The project follows Semantic Versioning.

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