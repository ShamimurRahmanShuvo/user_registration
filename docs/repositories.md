# Repositories

The repository abstraction isolates persistence from the registration
application service.

The core package defines the `UserRepository` protocol.

Required operations:

```text
create
get_by_id
get_by_username
get_by_email
exists_by_username
exists_by_email
update
delete
```

## Transaction ownership
The application owns the transaction.

A repository implementation must not call 
```python
session.commit()
```
or 
```python
session.rollback()
```
on the application's outer transaction.

The expected lifecycle is:
```text
Application
    |
    | begin transaction
    |
    +-- repository operation
    |
    +-- repository operation
    |
    | commit / rollback
    |
    +-- close
```

## Savepoints
A repository implementation may use a savepoint/nested transaction internally
when it needs to isolate an operation-level failure.

For example, the SQLAlchemy adapter uses a nested transaction to isolate
unique-constraint violations.

```text
Outer application transaction
          |
          +-- SAVEPOINT
          |      |
          |      +-- repository operation
          |      |
          |      +-- success -> release
          |      |
          |      +-- failure -> rollback savepoint
          |
          +-- application continues
```
This prevents an operation-level failure from unintentionally rolling back
unrelated application work.

## Duplicate Users

Repositories must enforce uniqueness for:
- username
- email

```python
DUplicateUserError
```
The registration service can then convert this into:
```python
RegistrationResult.duplicate(...)
```

## Application-Level Duplicate Checks
The registration service performs application-level checks:
```python
repository.exists_by_username(...)
repository.exists_by_email(...)
```
These checks improve user-facing behavior but do not replace database uniqueness constraints.

Therefore,
```text
Application check
       +
Database unique constraint
```
are both required.

## Repository Exceptions
Repository implementations should expose persistence-independent exceptions
through the core repository contract.

For example:

```python
DuplicateUserError
```

should be used instead of exposing:

```python
sqlalchemy.exc.IntegrityError
```
to the core registration service.

## Commit Behavior
Repositories do not commit successful operations.

For example:
```python
repository.create(user)

session.commit()
```
The application decides whether the transaction should be committed.

This makes the repository usable inside:

- HTTP requests
- background jobs
- CLI commands
- batch operations
- larger application transactions
- explicit transaction managers

## SQLAlchemy
The SQLAlchemy adapter uses:
```python
SQLAlchemyUserRepository(session)
```
The caller owns the Session lifecycle.

The repository does not create or close the session.

See [SQLAlchemy Integration](sqlalchemy.md)
