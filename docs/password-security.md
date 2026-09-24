# Password Security

## Storage

Plaintext passwords must never be stored.

```text
plaintext
   |
   v
password policy
   |
   v
Argon2 hash
   |
   v
password_hash
```

## Argon2

The default hasher is `Argon2Hasher`.

```python
Argon2Config(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)
```

Applications can explicitly configure these values when required by their security/performance policy.

## Verification

```python
hasher.verify(password, password_hash)
```

Mismatches and invalid hashes return `False`.

## Password policy

`PasswordValidatorAdapter` delegates password policy to `password-validator-s`.

## Security boundaries

The registration package does not implement authentication sessions, JWT, OAuth/OIDC, MFA, password reset, or account recovery.

Applications should never log plaintext passwords, password hashes, or authentication secrets.
