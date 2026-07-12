# multi-tenant-isolation — Current State

> Where things actually are **now**. The first doc a fresh agent reads to orient.
> Memory, not documentation — kept current every ticket. Pulled from `doc-patterns/living-docs/current-state.md`.

## What's built

- **Auth (T1)** — `get_caller` verifies a signed HS256 bearer token → `Caller{workspace_id, role, subject}`; **fails closed** on a missing key, missing token, bad signature, or missing claims (401). No unsigned/dev fallback.
- **Tenant-scoped store (T2)** — `ProjectStore` keyed by id; every `get/update/delete/list` takes a `workspace_id` and denies-by-default (a foreign id → None). `owner_of` exposes the owner for the audit trace only, never serialized.
- **CRUD endpoints (T3, T4)** — `GET/POST/PATCH/DELETE /projects[/{id}]`, all scoped; `GET /projects` cursor-paginated; delete is admin-only (403 in-tenant member); bad body → 422 (typed envelope).
- **Tenant isolation (T5)** — cross-tenant id → **404** on every verb; no other-workspace row serializes; **member cross-tenant delete → 404, not 403** (no existence oracle). Asserted by `test_isolation.py`.
- **Audit + boundary codemod (T6)** — `CROSS_TENANT_DENIED{workspace,target}` + `PROJECT_*` events; `require_caller_dep.py --check` enforces `Depends(get_caller)` on every route.

## What's in flight

- Nothing — all six tickets landed and green this session.

## Known gaps / not-yet-built

- **In-memory store only** — no DB/persistence; the isolation guard must be re-proven at a real query layer (see `decisions/0001`).
- **Tokens are verified, not minted** — no issuer, rotation, or user-management surface (out of scope; `open-questions.md`).
- **No rate limiting, no audit persistence** — events go to the in-process log + stderr only.

## How to run it

- Set up: `poetry install`.
- Configure the signing key: `export PROJECTS_JWT_SECRET=<a 32+ byte secret>`.
- Gate (no task-runner in this profile — the explicit `poetry run` block; see README "Run it").
- Launch: `poetry run uvicorn app.main:app --port 8000`.
- Tests: `poetry run pytest`.
