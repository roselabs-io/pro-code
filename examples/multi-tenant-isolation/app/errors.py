"""Typed error envelope — a chosen status + stable code, never a bare 500."""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse


class ApiError(Exception):
    """A failure with a deliberately-chosen status and a stable code."""

    def __init__(self, status: int, code: str, detail: str) -> None:
        self.status = status
        self.code = code
        self.detail = detail


def not_found() -> ApiError:
    """Cross-tenant or missing id — 404 hides existence, on every verb."""
    return ApiError(404, "not_found", "project not found")


def forbidden(detail: str) -> ApiError:
    """In-tenant role miss — 403, only ever returned after the scope check passes."""
    return ApiError(403, "forbidden", detail)


def unauthorized(detail: str) -> ApiError:
    """No valid caller — auth fails closed to 401."""
    return ApiError(401, "unauthorized", detail)


async def api_error_handler(_: Request, exc: ApiError) -> JSONResponse:
    """Serialize an ApiError to the typed {status, code, detail} envelope."""
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"status": exc.status, "code": exc.code, "detail": exc.detail}},
    )
