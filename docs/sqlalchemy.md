# SQLAlchemy Integration

Install:

```bash
pip install user-registration user-registration-sqlalchemy
```

The adapter maps the domain `User` to a SQLAlchemy model containing:

- UUID primary key
- unique username
- unique email
- password hash
- timestamps
- active flag

Repository:

```python
repository = SQLAlchemyUserRepository(session)
```

Mapping functions keep ORM objects out of the domain:

```python
to_domain(model)
to_model(user)
```

The database should enforce unique constraints on username and email.

`IntegrityError` uniqueness failures are translated into `DuplicateUserError`.

The application owns commit and rollback.

For complex outer transaction requirements, consider savepoints/nested transactions or a repository designed around the application's transaction manager.
