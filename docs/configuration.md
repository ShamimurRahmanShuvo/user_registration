# Configuration

`RegistrationConfig` controls registration behavior.

## Defaults

```python
RegistrationConfig(
    username_min_length=4,
    username_max_length=50,
    email_required=True,
    username_required=True,
    password_required=True,
    normalize_email=True,
    normalize_username=True,
)
```

## Environment variables

All variables use the `USER_REGISTRATION_` prefix:

```text
USER_REGISTRATION_USERNAME_MIN_LENGTH
USER_REGISTRATION_USERNAME_MAX_LENGTH
USER_REGISTRATION_EMAIL_REQUIRED
USER_REGISTRATION_USERNAME_REQUIRED
USER_REGISTRATION_PASSWORD_REQUIRED
USER_REGISTRATION_NORMALIZE_EMAIL
USER_REGISTRATION_NORMALIZE_USERNAME
```

Boolean values:

```text
true / false
1 / 0
yes / no
on / off
```

Example:

```bash
export USER_REGISTRATION_USERNAME_MIN_LENGTH=5
export USER_REGISTRATION_USERNAME_MAX_LENGTH=30
export USER_REGISTRATION_NORMALIZE_EMAIL=true
```

```python
config = RegistrationConfig.from_env()
```

Invalid values raise `ConfigurationError`.

The current `User` model requires username, email, and password hash. Therefore disabling those required fields should not be enabled until the domain contract explicitly supports passwordless or partial identities.
