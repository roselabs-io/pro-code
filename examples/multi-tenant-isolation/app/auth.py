"""Bearer-token auth resolved to a Caller at the request boundary.

A signed JWT carries the workspace, actor and role. ``get_caller`` is the boundary dep
every route takes (enforced by ``codemods/require_caller_dep.py``): no handler sees a
request without first resolving who is asking and which workspace they belong to.
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated

import jwt
from fastapi import Depends, Header
from pydantic import BaseModel

from app.config import TOKEN_ALGORITHM, token_secret
from app.errors import Unauthorized


class Role(str, Enum):
    MEMBER = "member"
    ADMIN = "admin"


class Caller(BaseModel):
    workspace_id: str
    actor_id: str
    role: Role


def issue_token(workspace_id: str, actor_id: str, role: Role) -> str:
    payload = {"ws": workspace_id, "sub": actor_id, "role": role.value}
    return jwt.encode(payload, token_secret(), algorithm=TOKEN_ALGORITHM)


def get_caller(authorization: Annotated[str | None, Header()] = None) -> Caller:
    if not authorization or not authorization.startswith("Bearer "):
        raise Unauthorized("Missing bearer token")
    token = authorization.removeprefix("Bearer ")
    try:
        payload = jwt.decode(token, token_secret(), algorithms=[TOKEN_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise Unauthorized("Invalid bearer token") from exc
    try:
        return Caller(
            workspace_id=payload["ws"],
            actor_id=payload["sub"],
            role=Role(payload["role"]),
        )
    except (KeyError, ValueError) as exc:
        raise Unauthorized("Malformed token claims") from exc


CallerDep = Annotated[Caller, Depends(get_caller)]
