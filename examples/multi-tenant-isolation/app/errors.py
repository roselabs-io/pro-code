"""Typed error envelope — every failure is a ``{status, code, detail}``, never a bare 500.

The status is chosen deliberately: a cross-tenant id returns 404, not 403, so it is
indistinguishable from a project that never existed — a 403 would leak existence.
"""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse


class ApiError(Exception):
    def __init__(self, status: int, code: str, detail: str) -> None:
        self.status = status
        self.code = code
        self.detail = detail


class NotFound(ApiError):
    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(404, "not_found", detail)


class Forbidden(ApiError):
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(403, "forbidden", detail)


class Unauthorized(ApiError):
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(401, "unauthorized", detail)


async def api_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, ApiError)
    return JSONResponse(
        status_code=exc.status,
        content={"status": exc.status, "code": exc.code, "detail": exc.detail},
    )
