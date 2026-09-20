"""
Configuration foundation.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, ClassVar, Mapping


class ConfigurationError(ValueError):
    """
    Raised when registration configuration is invalid
    """


def _parse_bool(value: str, name: str) -> bool:
    """
    Parse a boolean environment variable.
    Supported values:
        True: true, 1, yes, on
        False: false, 0, no, off
    """
    normalized = value.strip().lower()

    if normalized in {"true", "1", "yes", "on"}:
        return True

    if normalized in {"false", "0", "no", "off"}:
        return False

    raise ConfigurationError(
        f"{name} must be a boolean value (true/false, 1/0, yes/no, on/off); got {value!r}"
    )


def _parse_int(value: str, name: str) -> int:
    """
    Parse an integer environment variable
    """
    try:
        return int(value.strip())
    except ValueError as exc:
        raise ConfigurationError(
            f"{name} must be integer; got {value!r}"
        ) from exc
    
        
@dataclass(frozen=True, slots=True)
class RegistrationConfig:
    """
    Configuration for the user registration workflow.
    Password policy configuration doesn't belong here as it is delegated to the password-validator-s package.
    """
    username_min_length: int = 4
    username_max_length: int = 50
    
    email_required: bool = True
    username_required: bool = True
    password_required: bool = True
    
    normalize_email: bool = True
    normalize_username: bool = True
    
    ENV_PREFIX: ClassVar[str] = "USER_REGISTRATION_"
    
    def __post_init__(self) -> None:
        """Validate configuration after object construction"""
        if not self.username_required:
            raise ConfigurationError(
                "username_required=False is not supported"
            )

        if not self.email_required:
            raise ConfigurationError(
                "email_required=False is not supported"
            )

        if not self.password_required:
            raise ConfigurationError(
                "password_required=False is not supported"
            )

        if self.username_min_length < 1:
            raise ConfigurationError(
                "username_min_length must be greater than 0"
            )
        if self.username_max_length < self.username_min_length:
            raise ConfigurationError(
                "username_max_length must be greater than or equal to username_min_length"
            )
        
    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> RegistrationConfig:
        """
        Build registration configuration from environment variables.
        Args:
            environ: Optional environment mapping. If omitted, os.environ is used.
        Returns: 
            RegistrationConfig
        Raises:
            ConfigurationError: If an environment value cann't be parsed or the resulting configuration is invalid
        """
        source = os.environ if environ is None else environ
        prefix = cls.ENV_PREFIX
        
        values: dict[str, Any] = {}
        
        integer_fields = {
            "username_min_length": f"{prefix}USERNAME_MIN_LENGTH",
            "username_max_length": f"{prefix}USERNAME_MAX_LENGTH"
        }
        boolean_fields = {
            "email_required": f"{prefix}EMAIL_REQUIRED",
            "username_required": f"{prefix}USERNAME_REQUIRED",
            "password_required": f"{prefix}PASSWORD_REQUIRED",
            "normalize_email": f"{prefix}NORMALIZE_EMAIL",
            "normalize_username": f"{prefix}NORMALIZE_USERNAME"
        }
        
        for field_name, env_name in integer_fields.items():
            if env_name in source:
                values[field_name] = _parse_int(
                    source[env_name], env_name
                )
                
        for field_name, env_name in boolean_fields.items():
            if env_name in source:
                values[field_name] = _parse_bool(
                    source[env_name], env_name
                )
                
        return cls(**values)
