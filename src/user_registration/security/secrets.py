from __future__ import annotations

import secrets


def generate_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.
    This utility is intentionally generic. Authentication, password reset, email verification, etc. belong in
    separate packages.
    """
    if length < 16:
        raise ValueError("Token length must be at lease 16 bytes")

    return secrets.token_urlsafe(length)
