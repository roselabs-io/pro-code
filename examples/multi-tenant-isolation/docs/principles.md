# Multi-tenant Projects API — Principles

> The values that bias every fork, before any rule. `generic-saas` profile.

## Universal

- **Grade the context, not just the code.** Every handoff passed a grader.
- **Author ≠ grader.** Nothing graded its own work.
- **No done without fresh evidence.** "Passes" = the test command showed zero failures this session.
- **Fail loudly.** A silent wrong answer is worse than a loud stop.
- **Every correction given twice is a missing grader.** (The boundary-dep rule became a codemod.)

## Domain values (`generic-saas`)

- **Deny by default.** An unscoped path returns nothing, not a leak. The store has no accessor that
  reaches a row without a `workspace_id`; a foreign id is `None`.
- **Enforce at the boundary, not the caller.** Isolation + RBAC live server-side at the request
  boundary (`get_caller` + the scoped store), never trusted to the client.
- **A denied cross-tenant id must be indistinguishable from not-found.** 404 before 403 — a 403
  would leak that the resource exists.
