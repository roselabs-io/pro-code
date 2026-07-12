"""Auth resolver — verify the signed bearer token, resolve it to a Caller, fail closed.

A missing key or a bad token DENIES; there is no unsigned or dev-open fallback in the
gated path — the boundary trusts a valid signature only.
"""

from __future__ import annotations

import jwt
from fastapi import Header

from app.config import JWT_ALGORITHM, jwt_secret
from app.errors import unauthorized
from app.models import Caller

ADMIN = "admin"
MEMBER = "member"
_ROLES = frozenset({ADMIN, MEMBER})


def get_caller(authorization: str | None = Header(default=None)) -> Caller:
    """Resolve the bearer token to a Caller — deny on a missing key or bad token."""
    secret = jwt_secret()
    if secret is None:
        raise unauthorized("auth is not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise unauthorized("missing bearer token")

    token = authorization.removeprefix("Bearer ").strip()
    try:
        claims = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise unauthorized("invalid token") from None

    workspace_id = claims.get("workspace_id")
    role = claims.get("role")
    subject = claims.get("sub")
    if not workspace_id or role not in _ROLES or not subject:
        raise unauthorized("token missing required claims")
    return Caller(workspace_id=workspace_id, role=role, subject=subject)
