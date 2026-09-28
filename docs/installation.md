# Installation

## Requirements

The packages require:

- Python 3.12 or later

The adapters additionally require their respective integration dependencies.

## Core Package

Install the core registration package:

```bash
pip install user-registration
```
The core package provides:

- registration domain models
- registration service
- validation
- password hashing abstractions
- Argon2 implementation
- repository protocol
- registration hooks
- configuration

## FastAPI Adapter
Install:
```bash
pip install user-registration-fastapi
```
The adapter provides FastAPI-specific:
- request models
- response models
- dependency integration
- HTTP status mapping
- registration router

The adapter depends on:
```markdown
user-registration
fastapi
```

## SQLAlchemy Adapter
Install:
```bash
pip install user-registration-sqlalchemy
```
The adapter provides:
- SQLAlchemy user model
- domain/ORM mapping
- SQLAlchemy repository implementation
- duplicate-user exception translation

The adapter depends on:
```markdown
user-registration
sqlalchemy
```

## FastAPI + SQLAlchemy

For an application using both integrations:
```bash
pip install user-registration-fastapi user-registration-sqlalchemy
```
The resulting architecture is:
```markdown
                  FastAPI
                     |
                     v
       user-registration-fastapi
                     |
                     v
          RegistrationService
                     |
                     v
       user-registration-sqlalchemy
                     |
                     v
                 SQLAlchemy
                     |
                     v
                 Database
```

##Development Installation

Clone the repository:

```bash
git clone https://github.com/ShamimurRahmanShuvo/user_registration.git
cd user_registration
```

Create a virtual environment:

`python3.14 -m venv .venv`

Install the core package with development dependencies:

`.venv/bin/python -m pip install -e ".[dev]"`

Install FastAPI adapter development dependencies:

`.venv/bin/python -m pip install -e "./adapters/fastapi[dev]"`

Install SQLAlchemy adapter development dependencies:

`.venv/bin/python -m pip install -e "./adapters/sqlalchemy[dev]"`

Verify Installation

`.venv/bin/python -c "import user_registration; print(user_registration.__version__)"`

Verify the FastAPI adapter:

`.venv/bin/python -c "import user_registration_fastapi; print('FastAPI adapter OK)"`

Verify the SQLAlchemy adapter:

`.venv/bin/python -c "import user_registration_sqlalchemy; print('SQLAlchemy adapter OK')"`

### Supported Python Versions

The project currently targets:
```markdown
Python 3.12
Python 3.13
Python 3.14
```
CI validates the supported Python versions.