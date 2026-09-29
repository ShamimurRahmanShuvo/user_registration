# SQLAlchemy Integration

Install:

```bash
pip install user-registration-sqlalchemy
```
The SQLAlchemy adapter provides a synchronous SQLAlchemy 2.x implementation
of the UserRepository protocol.

The adapter maps the domain `User` to a SQLAlchemy model containing:

- UUID primary key
- unique username
- unique email
- password hash
- timestamps
- active flag

## Repository:

```python
from user_registration_sqlalchemy import SQLAlchemyUserRepository

repository = SQLAlchemyUserRepository(session)
```
The caller provides the SQLAlchemy Session.

The repository does not:
- create the session
- close the session
- commit the session
- roll back the application's outer transaction

## Transaction Ownership
The application owns the outer transaction.

Example
```python
session = Session(engine)

try:
    repository = SQLAlchemyUserRepository(session)

    result = repository.create(user)

    session.commit()

except Exception:
    session.rollback()
    raise

finally:
    session.close()
```

## Nested Transaction
The repository uses SQLAlchemy nested transactions for operations that may fail because of uniqueness constraints.

For example:
```text
outer transaction
      |
      +-- repository.create()
              |
              +-- SAVEPOINT
                     |
                     +-- INSERT
                     |
                     +-- IntegrityError
                     |
                     +-- rollback SAVEPOINT
```
The outer transaction remains under application control.

## Uniqueness
The SQLAlchemy model defines unique constraints for:

```text
username
email
```

The database remains the final authority for uniqueness.

Application-level existence checks do not eliminate race conditions.

## DuplicateUserError

SQLAlchemy:
```python
IntegrityError
```
is translated by the adapter into:
```python
DuplicateUserError
```
This prevents SQLAlchemy-specific exceptions from leaking into the core
registration service.

## Domain / ORM Separation

The domain User is separate from the SQLAlchemy UserModel.

Mapping functions provide the boundary:

```python
to_domain(model)
to_model(user)
```
The core package therefore does not depend on SQLAlchemy.

## Update Behavior

Updating username or email can also violate unique constraints.

The adapter translates those violations into:
```python
DuplicateUserError
```

## Async SQLAlchemy

The current adapter uses synchronous:
```python
sqlalchemy.orm.Session
```
Async SQLAlchemy is not part of the current adapter contract.
