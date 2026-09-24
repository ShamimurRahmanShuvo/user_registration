# Repositories

The repository abstraction isolates persistence from registration logic.

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

Database repositories should enforce unique constraints for username and email.

Persistence uniqueness failures should be translated to:

```python
DuplicateUserError
```

The application owns transactions:

```text
begin
  -> register
  -> commit / rollback
  -> close
```

The core does not assume SQLAlchemy or any specific database.

The SQLAlchemy implementation is provided by `user-registration-sqlalchemy`.
