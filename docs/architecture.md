# Architecture

## Purpose

`user-registration` separates registration business logic from application frameworks and persistence technologies.

The core package contains the domain and application logic.

Infrastructure integrations are implemented as adapters.

## Architectural Layers

```text
+------------------------------------------------+
|                Application                     |
|                                                |
| FastAPI / Django / Flask / CLI / Other        |
+-----------------------+------------------------+
                        |
                        v
+------------------------------------------------+
|              Registration Core                 |
|                                                |
| RegistrationService                            |
| User                                            |
| RegistrationRequest                             |
| RegistrationResult                              |
| ValidationRegistry                              |
| PasswordHasher Protocol                         |
| UserRepository Protocol                         |
| RegistrationHook Protocol                       |
+-----------------------+------------------------+
                        |
                        v
+------------------------------------------------+
|                 Adapters                       |
|                                                |
| SQLAlchemy / FastAPI / Future adapters         |
+------------------------------------------------+