# projects — Surface Spec

> One drill-down per surface — here a "surface" is the **group of `/projects` API endpoints**.
> Sketch-shaped: enough for Implement to start. Pulled from `doc-patterns/specs/surface-spec.md`.

## What it does

- **Purpose:** CRUD over a workspace's projects, isolated per tenant.
- **Actors:** `member` (read + create + update), `admin` (member + delete). Both resolved from the bearer token.
- **Shows / returns:** `Project{id, workspace_id, name, description, created_at}`; lists return a cursor page `{items, next_cursor}`.

## Controls / inputs

| Control / input | Triggers | Notes / validation |
|---|---|---|
| `GET /projects?cursor=&limit=` | list own-workspace projects | `limit` clamped to `[1, MAX_PAGE_SIZE]`; default `DEFAULT_PAGE_SIZE`; `cursor` opaque |
| `POST /projects` | create a project in own workspace | body `{name, description?}`; `name` required, 1–`MAX_NAME_LEN` chars → else 422 |
| `GET /projects/{id}` | read one, scoped | cross-tenant / missing id → 404 |
| `PATCH /projects/{id}` | update mutable fields, scoped | body `{name?, description?}`; empty body → 422; cross-tenant → 404 |
| `DELETE /projects/{id}` | delete, scoped, **admin-only** | cross-tenant → 404 (scope before role); in-tenant + member → 403 |

## Calls + contracts

- `GET /projects` → `200 {items: [Project], next_cursor: str|null}`
- `POST /projects` → `201 Project`; `422 {error}` on invalid body
- `GET /projects/{id}` → `200 Project`; `404 {error}` cross-tenant/missing
- `PATCH /projects/{id}` → `200 Project`; `404` cross-tenant/missing; `422` empty/invalid body
- `DELETE /projects/{id}` → `204`; `404` cross-tenant/missing; `403` in-tenant member
- All auth failures → `401 {error}` (missing/invalid token or unconfigured key)

## States

- **Empty:** `GET /projects` with no projects → `200 {items: [], next_cursor: null}`.
- **Loading:** n/a (synchronous in-memory).
- **Error:** invalid body → `422` typed envelope; unexpected → typed `500`, never a leaked stack.
- **Permission-denied:** cross-tenant → **404** (hides existence); in-tenant role miss → **403**. The 404-before-403 ordering is the load-bearing rule.

## Design shapes referenced

- `tenant-scoped-query-guard` — scope every verb by `workspace_id`, deny-by-default.
- `rbac-check-at-boundary` — delete gated on `admin`, enforced at the request boundary, **after** the scope check.
- `structured-error-envelope` — typed `{status, code, detail}`, 404 vs 403 chosen deliberately.
- `cursor-pagination` — stable cursor paging on the list.
- `severity-tiered-validation` — request-body validation (blocking → 422).
- `write-through-audit-log` — `CROSS_TENANT_DENIED` + `PROJECT_*` events emitted as the write lands.
