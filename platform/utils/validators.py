import re
from typing import Annotated

from annotated_types import Len
from pydantic import (
    AfterValidator,
    SecretStr,
)


# Custom type for strong passwords
def validate_strong_password(value: str | SecretStr) -> str:
    """Validate password meets complexity requirements."""
    val = value.get_secret_value() if isinstance(value, SecretStr) else value
    if len(val) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", val):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", val):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", val):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[@$!%*?&]", val):
        raise ValueError(
            "Password must contain at least one special character (@$!%*?&)"
        )
    return val


StrongPassword = Annotated[
    SecretStr,  # Stores password securely (not plaintext)
    Len(min_length=8, max_length=128),
    AfterValidator(validate_strong_password),
]
