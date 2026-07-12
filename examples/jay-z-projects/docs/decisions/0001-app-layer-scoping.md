# 0001 — Scope isolation at the app/store layer, not a database

> A durable decision + the load-bearing why. Pulled from `doc-patterns/living-docs/decision-record.md`.

- **Status:** accepted
- **Date:** 2026-07-11
- **Ticket:** T2 / T5

## Context

The core promise is *no cross-tenant leak*. Isolation can be enforced in the datastore (Postgres row-level security) or in the application's query layer (every query scoped by `workspace_id`). The slice has no database.

## Decision

- Enforce isolation in the **store layer**: every `ProjectStore` method takes a `workspace_id`, and a foreign id resolves to `None` (deny-by-default). Handlers can only serialize what the scoped store hands back.

## Why (and what we rejected)

- RLS is stronger defense-in-depth but couples the slice to Postgres and needs infra to test. The app-layer guard is **verifiable by an integration test today** (`test_isolation.py`), which is what the pipeline grades on. The guard shape (scope-by-tenant) is identical to what a scoped ORM or RLS policy would express, so the proof transfers.
- **Consequence:** a real deployment with a DB must re-prove isolation at the query layer (backlog N1). The in-memory store is the slice's boundary, not a production claim.

## Consequences

- Isolation lives in one place (`store.py`), easy to audit and codemod-guard.
- Adding a second data store means re-running the isolation proof against it before trusting it.
