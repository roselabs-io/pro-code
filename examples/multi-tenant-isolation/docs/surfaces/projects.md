# Projects endpoints — Surface Spec

> Surface = the group of `/projects` API endpoints (`generic-saas`: a surface is an endpoint group).

## What it does

- **Purpose:** CRUD over projects, every operation scoped to the caller's workspace.
- **Actors:** member (all but delete), admin (all). Resolved from the bearer token at the boundary.
- **Shows / returns:** `ProjectOut` rows; `ProjectPage` for the list; the typed error envelope on failure.

## Controls / inputs

| Control / input | Triggers | Notes / validation |
|---|---|---|
| `POST /projects` `{name, description?}` | create in caller's workspace | `name` 1–200 chars → else 422 |
| `GET /projects?cursor=&limit=` | list caller's workspace | `limit` 1–200 → else 422 |
| `GET /projects/{id}` | fetch one own row | foreign/absent id → 404 |
| `PATCH /projects/{id}` `{name?, description?}` | partial update | foreign/absent id → 404 |
| `DELETE /projects/{id}` | delete (admin only) | member → 403; foreign id → 404 (before role) |

## Calls + contracts

- `POST /projects` → `201 {id, workspace_id, name, description, created_by}`.
- `GET /projects` → `200 {items: [...], next_cursor: str | null}`.
- `GET|PATCH /projects/{id}` → `200 ProjectOut`, or `404 {status, code, detail}`.
- `DELETE /projects/{id}` → `204`, or `403` (member), or `404` (foreign/absent).

## States

- **Empty:** list returns `{items: [], next_cursor: null}`.
- **Loading:** n/a (synchronous in-memory).
- **Error:** typed envelope `{status, code, detail}`; validation errors are pydantic 422.
- **Permission-denied:** cross-tenant → **404** (indistinguishable from not-found; emits
  `CROSS_TENANT_DENIED`). Member delete → **403** (emits `RBAC_DENIED`).

## Design shapes referenced

- `tenant-scoped-query-guard` · `rbac-check-at-boundary` · `structured-error-envelope` ·
  `write-through-audit-log` · `cursor-pagination`.
