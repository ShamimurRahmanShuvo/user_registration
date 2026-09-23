# Configuration

## RegistrationConfig

`RegistrationConfig` controls registration behavior.

```python
from user_registration import RegistrationConfig

config = RegistrationConfig(
    username_min_length=4,
    username_max_length=50,
    email_required=True,
    username_required=True,
    password_required=True,
    normalize_email=True,
    normalize_username=True,
)