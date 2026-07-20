import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.log import log_event
from app.core.security import decode_token
from app.models.author import Author
from app.repositories.authors import AuthorRepository

_bearer = HTTPBearer(auto_error=False)


def _unauthorized(reason: str) -> HTTPException:
    log_event("AUTH_DENIED", reason=reason)
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
    )


async def get_current_author(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    session: AsyncSession = Depends(get_session),
) -> Author:
    if credentials is None:
        raise _unauthorized("missing_token")
    try:
        payload = decode_token(credentials.credentials)
    except jwt.PyJWTError:
        raise _unauthorized("invalid_token") from None
    try:
        author_id = uuid.UUID(str(payload.get("sub")))
    except ValueError:
        raise _unauthorized("bad_subject") from None
    author = await AuthorRepository(session).get_by_id(author_id)
    if author is None:
        raise _unauthorized("unknown_subject")
    return author
