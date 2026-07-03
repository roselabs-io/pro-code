# 0001 — Enforce isolation at the app layer, not the datastore

- **Status:** accepted
- **Date:** 2026-07-03
- **Ticket:** T2 (workspace-scoped store), T7 (isolation invariant)

## Context

Isolation is the core promise. It can be enforced at the datastore (Postgres row-level security)
or at the application layer (a store whose every accessor is scoped by `workspace_id`). This slice
has no datastore — state is in-memory — so the datastore option isn't even on the table yet.

## Decision

Enforce isolation at the app layer: `ProjectStore` exposes **no** accessor that reaches a row
without a `workspace_id`, and a lookup for a foreign id returns `None` (deny-by-default). The
routes pass `caller.workspace_id` on every call.

## Why (and what we rejected)

- **Rejected — Postgres RLS:** stronger defense-in-depth, but couples the slice to a specific DB,
  can't run in-memory, and complicates the local isolation test. Not available with no DB anyway.
- The app-layer guard is **verifiable by an integration test today** (the hard-done bar) and the
  shape is datastore-agnostic — when a DB is added, the same "no unscoped accessor" rule carries
  over, and RLS can be layered under it for defense-in-depth. Revisit then.

## Consequences

- The isolation invariant is proven by `test_isolation.py` hitting the real query path.
- A future DB migration must preserve the "no unscoped accessor" contract, or add RLS beneath it.
