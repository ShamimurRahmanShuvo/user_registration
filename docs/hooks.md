# Registration Hooks

Hooks execute after successful registration.

```python
class RegistrationHook(Protocol):
    def after_registration(self, user: User) -> None:
        ...
```

Example:

```python
class WelcomeHook:
    def after_registration(self, user: User) -> None:
        print(f"Welcome {user.username}")

service = RegistrationService(
    repository=repository,
    password_hasher=Argon2Hasher(),
    password_validator=PasswordValidatorAdapter(),
    hooks=(WelcomeHook(),),
)
```

Suitable uses include application events, audit events, non-critical notifications, and cache invalidation.

For critical external operations, an outbox or event-driven design is preferable to making registration depend directly on a remote service.

Applications should decide how hook failures interact with their transaction policy.
