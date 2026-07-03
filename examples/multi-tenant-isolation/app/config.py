"""Named configuration — limits and env keys live here, never as literals in the code."""

from __future__ import annotations

import os

# Signing secret for bearer tokens. A dev default keeps local runs and tests turnkey;
# production overrides it via the environment.
TOKEN_SECRET_ENV = "APP_TOKEN_SECRET"
DEV_TOKEN_SECRET = "dev-secret-not-for-production-000000000000"

# HS256: symmetric HMAC-SHA256 — one shared secret verifies every workspace's tokens.
TOKEN_ALGORITHM = "HS256"

# Pagination — a project list can grow unbounded, so it pages with an opaque cursor.
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 200


def token_secret() -> str:
    return os.environ.get(TOKEN_SECRET_ENV, DEV_TOKEN_SECRET)
