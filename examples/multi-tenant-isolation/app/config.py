"""Named config — limits and the signing key, never magic literals in the code."""

from __future__ import annotations

import os

# Pagination bounds.
MIN_PAGE_SIZE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Project-name validation bounds.
MIN_NAME_LEN = 1
MAX_NAME_LEN = 120

# The bearer token's signing algorithm.
JWT_ALGORITHM = "HS256"

_JWT_ENV_VAR = "PROJECTS_JWT_SECRET"


def jwt_secret() -> str | None:
    """Return the signing secret, or None when unset — auth fails closed on None."""
    secret = os.environ.get(_JWT_ENV_VAR)
    return secret or None
