"""Typed error envelope — a status you chose and a stable code, never a bare 500."""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse


class ApiError(Exception):
    """A failure that carries a status you picked on purpose and a stable code."""

    def __init__(self, status: int, code: str, detail: str) -> None:
        self.status = status
        self.code = code
        self.detail = detail


def not_found() -> ApiError:
    """Cross-tenant or missing id — 404 keeps existence a secret, every verb."""
    return ApiError(404, "not_found", "project not found")


def forbidden(detail: str) -> ApiError:
    """In-tenant role miss — 403, and only after the scope check already let you in."""
    return ApiError(403, "forbidden", detail)


def unauthorized(detail: str) -> ApiError:
    """No real caller — auth fails closed, straight to 401."""
    return ApiError(401, "unauthorized", detail)


async def api_error_handler(_: Request, exc: ApiError) -> JSONResponse:
    """Dress an ApiError up as the typed {status, code, detail} envelope."""
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"status": exc.status, "code": exc.code, "detail": exc.detail}},
    )
