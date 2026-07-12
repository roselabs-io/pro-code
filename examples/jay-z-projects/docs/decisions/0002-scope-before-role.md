# 0002 — Check tenant scope BEFORE the role gate (no existence oracle)

> A durable decision + the load-bearing why. Pulled from `doc-patterns/living-docs/decision-record.md`.

- **Status:** accepted
- **Date:** 2026-07-11
- **Ticket:** T4 / T5

## Context

`DELETE /projects/{id}` is admin-only. A handler must apply two checks — tenant scope (→404) and the role gate (→403). The **order** is load-bearing: it decides whether a cross-tenant probe can learn that a foreign id exists.

## Decision

- **Scope first, role second.** The handler fetches the project *scoped by the caller's workspace*; a miss is a 404 (indistinguishable from nonexistent). Only once the resource is confirmed in-tenant does the role gate run and possibly return 403.

## Why (and what we rejected)

- The rejected order (role gate first, or a global fetch then role) leaks existence: a member probing cross-tenant ids would get 403 for *existing* foreign ids and 404 for missing ones — a 403-vs-404 **oracle** across the tenant boundary. Scope-first collapses both to 404, so a 403 is only ever seen for an in-tenant resource.
- Asserted by `test_member_cross_tenant_delete_is_404_not_403` — the adversarial refutation target.

## Consequences

- 403 is a safe signal: its mere presence reveals the resource is in *your* workspace, which you already knew.
- Every verb that gates on role must keep the scope check first; the drift grader watches for a reordering.
