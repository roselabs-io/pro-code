# jay-z-projects — System Overview

> The 30,000-foot picture: the system's shape, its dataflows, its boundaries.
> Pulled from `doc-patterns/specs/system-overview.md`; filled from the functional analysis.

## Components

| Component | What it does |
|---|---|
| Auth resolver (`app/auth.py`) | verifies the signed bearer token, resolves it to a `Caller{workspace_id, role, subject}`; **fails closed** on a missing/invalid key or bad token |
| Tenant-scoped store (`app/store.py`) | in-memory project store; **every** query takes a `workspace_id` and returns only matching rows — deny-by-default is enforced here, not in the handlers |
| Request boundary (`app/main.py`) | FastAPI routes; every route depends on `get_caller`; scopes at the store, then applies the role gate |
| Error envelope (`app/errors.py`) | typed `{status, code, detail}` responses; chooses 404 vs 403 deliberately; no bare 500 for expected failures |
| Structured log (`app/log.py`) | emits stable-code events (`PROJECT_CREATED`, `CROSS_TENANT_DENIED`, …) the logs grader reads |
| Boundary codemod (`codemods/require_caller_dep.py`) | deterministic check that **every** route carries the `get_caller` dependency (drift can't sneak an unguarded route in) |

## Key dataflows

- **CRUD:** caller → `get_caller` resolves the token → handler calls the store **scoped by `caller.workspace_id`** → store returns only in-workspace rows → handler applies any role gate → typed response; a write emits a `PROJECT_*` log event.
- **Cross-tenant denial:** caller of A requests B's id → the scoped store lookup misses (deny-by-default) → handler emits `CROSS_TENANT_DENIED{workspace,target}` and returns **404** → no B row is ever serialized, on every verb.

## Integration boundaries

- **Token issuer** — inbound. This slice only **verifies**: it reads a bearer token, validates the signature against a shared secret, and trusts the claims (`workspace_id`, `role`, `sub`). It does not mint tokens or call the issuer. Contract: a signed JWT (HS256 — build choice, see assumptions). A missing secret or bad signature → **deny** (fail closed), never a dev-open fallback.

## Tech-stack call-outs

- **In-memory store instead of a database** — the slice proves the *isolation guard*, which is a query-scoping property; an in-memory dict scoped by `workspace_id` exercises the same guard shape a DB would, with no infra. A real deployment re-proves the guard at the DB layer (RLS or a scoped ORM). *(See `decisions/0001`.)*
- **HS256 signed bearer token** — the profile declares the token library + algorithm are a build choice; HS256 via PyJWT is recorded in the assumptions ledger. *(See `decisions/0002`.)*
