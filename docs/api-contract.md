# API Contract

## Overview

`user-registration` provides a framework-agnostic user registration
workflow for Python applications.

The package does not depend on:

- FastAPI
- Django
- Flask
- SQLAlchemy
- Django ORM
- PostgreSQL
- MySQL
- MongoDB
- Redis

Framework and database integrations are implemented outside the core package.

---

# Configuration

The primary configuration object is:

```python
from user_registration import RegistrationConfig

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

```
