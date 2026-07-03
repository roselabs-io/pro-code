# Multi-tenant Projects API — System Overview

> The 30,000-foot picture. Plan's output, from the functional analysis.

## Components

| Component | What it does |
|---|---|
| `get_caller` boundary dep (`app/auth.py`) | resolves the signed bearer token to a `Caller` (workspace, actor, role); every route depends on it (codemod-enforced) |
| Error envelope (`app/errors.py`) | typed `{status, code, detail}`; a cross-tenant miss returns 404, never a bare 500/403 |
| Workspace-scoped store (`app/store.py`) | the `tenant-scoped-query-guard`: no accessor reaches a row without a `workspace_id`; a foreign id resolves to `None` |
| Projects routes (`app/main.py`) | the endpoint group; isolation + RBAC enforced at the boundary |
| Structured event log (`app/log.py`) | emits `PROJECT_*` / `CROSS_TENANT_DENIED` / `RBAC_DENIED` for the logs grader |
| Named config (`app/config.py`) | page sizes, token secret/algorithm — no magic numbers in code |

## Key dataflows

- **Create/read/update/list:** request + bearer token → `get_caller` resolves the workspace →
  the route calls the store with `caller.workspace_id` → a scoped row (or an empty page) →
  a `PROJECT_*` event fires as the write lands → serialized `ProjectOut`.
- **Cross-tenant / role denial:** request references a foreign id (or a member tries delete) →
  the scoped store returns `None` (or the role check fails) → `CROSS_TENANT_DENIED` /
  `RBAC_DENIED` fires → 404 / 403 envelope. Isolation is checked **before** role, so a foreign
  id is 404 even to an admin.

## Integration boundaries

- **Token issuer (inbound).** Protocol: HTTP `Authorization: Bearer <JWT>`. Trigger: every request.
  Payload: a JWT signed HS256 with claims `{ws, sub, role}`. An absent/invalid/tampered token → 401.
  The issuer is out of repo; this service only *verifies* tokens (shared secret). See `decisions/0002`
  and the open question on asymmetric signing.

## Tech-stack call-outs

- **In-memory store instead of a datastore** — the isolation slice is proven at the app layer; the
  scoped-query-guard shape is datastore-agnostic and carries over to a DB. See `decisions/0001`.
