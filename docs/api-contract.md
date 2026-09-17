# API Contract

## Overview

`user-registration` provides a framework-agnostic user registration
workflow for Python applications' registration workflow.

The package does not depend on:

- Web framework
- Database
- ORM
- Authentication system
- API framework

Framework and database integrations are implemented outside the core package.

---
# UserRepository
The `UserRepository` protocol defines the persistence boundary for users

# RegistrationRequest
`RegistrationRequest` represents data submitted for user registration.

# Configuration

The primary configuration object is:

```python
from user_registration import RegistrationConfig
from user_registration import RegistrationRequest
from user_registration import UserRepository
```

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


