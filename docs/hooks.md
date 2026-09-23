# Registration Hooks

Registration hooks allow applications to execute additional behavior after successful persistence.

## Contract

```python
class RegistrationHook(Protocol):
    def after_registration(self, user: User) -> None:
        ...