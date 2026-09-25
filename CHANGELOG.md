# Changelog

## [0.1.2] - 2026-09-25
Release with ruff fix for adapters and add Adapters documentation.

## [0.1.1] - 2026-09-25
Initial alpha release with fix GitHub actions workflow

## [0.1.0] - 2026-09-23
Initial alpha release

### Added

- Framework-independent user registration service
- Database-independent domain model
- Registration request and result models
- Environment-based configuration
- Username validation
- Email validation
- Extensible validation registry
- Password policy integration with `password-validator-s`
- Argon2 password hashing
- Password hasher protocol
- Password validator protocol
- User repository protocol
- Repository error abstractions
- Duplicate-user detection
- Registration hooks
- Registration result statuses
- Security token utility
- SQLAlchemy adapter
- FastAPI adapter
- Unit test suite
- Integration test suite
- mypy configuration
- Ruff configuration
- Package build configuration


### Scope

The core intentionally excludes login, sessions, JWT, OAuth, MFA, RBAC, password reset, and framework-specific routing.