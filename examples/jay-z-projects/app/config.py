"""Named config — every limit wears a name; no loose numbers running in this code."""

from __future__ import annotations

import os

# Page bounds — how many rows you get, floor to ceiling.
MIN_PAGE_SIZE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Name bounds — too short or too long and the name don't make the cut.
MIN_NAME_LEN = 1
MAX_NAME_LEN = 120

# The house algorithm that signs the bearer token.
JWT_ALGORITHM = "HS256"

_JWT_ENV_VAR = "PROJECTS_JWT_SECRET"


def jwt_secret() -> str | None:
    """Hand back the signing key, or None when it's unset — no key, we fail closed."""
    secret = os.environ.get(_JWT_ENV_VAR)
    return secret or None
