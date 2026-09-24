# Validation

Validation uses `FieldValidator` and `ValidationRegistry`.

## Default validators

### UsernameValidator

Defaults:

- Minimum length: 3
- Maximum length: 50
- Pattern: `^[a-zA-Z0-9_.-]+$`

### EmailValidator

The default validator requires a non-empty local part, `@`, a domain, and a dot in the domain. It is intentionally lightweight and is not a complete RFC email parser.

## Custom validators

```python
class ReservedUsernameValidator:
    def validate(self, value: str) -> str | None:
        if value == "admin":
            return "Username is reserved"
        return None
```

Register it:

```python
config = RegistrationConfig()
registry = create_default_validation_registry(config)
registry.register("username", ReservedUsernameValidator())

service = RegistrationService(
    repository=repository,
    password_hasher=Argon2Hasher(),
    password_validator=PasswordValidatorAdapter(),
    config=config,
    validation_registry=registry,
)
```

Multiple validators can be registered for a field. Errors are collected.

Field names are case-insensitive.

Registration validation order is:

1. required fields
2. normalization
3. field validation
4. duplicate checks
5. password validation
