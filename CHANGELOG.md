
# Changelog

All notable changes to this project will be documented in this file.

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