"""Public API for the user-registration package."""
from user_registration.config import (
    ConfigurationError,
    RegistrationConfig
)
from user_registration.exceptions import (
    RegistrationError,
    UserAlreadyExistsError
)
from user_registration.models import (
    RegistrationRequest,
    User
)
from user_registration.password import (
    Argon2Hasher,
    PasswordHasher,
    PasswordPolicyValidator,
    PasswordValidatorAdapter
)
from user_registration.registration import (
    NoOpRegistrationHook,
    RegistrationHook,
    RegistrationResult,
    RegistrationService
)
from user_registration.repository import UserRepository
from user_registration.validation import (
    EmailValidator,
    FieldValidator,
    UsernameValidator,
    ValidationError,
    ValidationRegistry,
    create_default_validation_registry
)


__version__ = "0.1.0"

__all__ = [
    "__version__",
    "ConfigurationError",
    "RegistrationConfig",
    "RegistrationRequest",
    "User",
    "UserRepository",
    "PasswordHasher",
    "Argon2Hasher",
    "PasswordPolicyValidator",
    "PasswordValidatorAdapter",
    "RegistrationError",
    "UserAlreadyExistsError",
    "RegistrationResult",
    "RegistrationService",
    "RegistrationHook",
    "NoOpRegistrationHook",
    "FieldValidator",
    "ValidationError",
    "UsernameValidator",
    "EmailValidator",
    "ValidationRegistry",
    "create_default_validation_registry"
]
