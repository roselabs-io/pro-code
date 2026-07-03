# Multi-tenant Projects API — Current State

> Where things actually are now. The first doc a fresh agent reads. Kept current every ticket.

## What's built

- **Auth boundary** — `get_caller` resolves a signed JWT (HS256) to a `Caller{workspace, actor,
  role}`; missing/invalid/tampered → 401. Every route depends on it (codemod-enforced).
- **Workspace-scoped store** — in-memory; every accessor takes a `workspace_id`; a foreign id
  resolves to `None`. No unscoped accessor exists.
- **Projects endpoints** — create (201), read, list (cursor-paginated), update (PATCH), delete
  (admin-only, 204). Typed error envelope on every failure.
- **Tenant isolation** — cross-tenant read/list/write all 404; a foreign id is byte-identical to a
  pure miss; certified by `tests/test_isolation.py`.
- **Observability** — `PROJECT_CREATED/UPDATED/DELETED`, `CROSS_TENANT_DENIED`, `RBAC_DENIED`
  structured events; asserted by `tests/test_logs_grader.py`.

## What's in flight

- Nothing — the slice is complete and the gate is green (27 tests).

## Known gaps / not-yet-built

- **No persistence** — in-memory; state resets on restart.
- **No workspace lifecycle** — workspaces + actor assignment live upstream (token issuer).
- **Symmetric token signing (HS256)** — assumes the issuer shares the secret; see `assumptions.md`.
- **No PUT / bulk / soft-delete** — only the verbs above.

## How to run it

```bash
poetry install
# gate (deterministic graders, in short-circuit order):
poetry run ruff check --fix app tests codemods && poetry run ruff format app tests codemods
poetry run ruff check app tests codemods
poetry run python ../../graders/checks/doctrine_lint.py app tests
poetry run python ../../graders/checks/doctrine_lint.py app \
  --forbid 'print\(@@use LOG' --forbid 'except\s*:@@no bare except'
poetry run python codemods/require_caller_dep.py --check app/main.py
poetry run pytest -q
# launch:
poetry run uvicorn app.main:app --port 8000
```
