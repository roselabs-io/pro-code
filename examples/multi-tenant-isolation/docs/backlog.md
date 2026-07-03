# Multi-tenant Projects API — Backlog

> One row per functionality, each well-formed: a verifiable acceptance criterion, a design hook
> (or `novel`), `depends-on`, an autonomy tier. Forward-only — shipped rows are deleted (git is
> the record). **All tickets below shipped; retained here as the delivered slice's record.**

## Tickets

| ID | Title | Acceptance criterion (verifiable) | Design hooks | Depends on | Autonomy |
|---|---|---|---|---|---|
| T1 | Auth boundary + Caller | missing/invalid/tampered bearer → 401; a valid token resolves `{ws, sub, role}`; asserted by `test_auth.py` | `novel — author fresh` (JWT verify) | — | 🟡 auth boundary — agent-draft, human confirms the token contract |
| T2 | Workspace-scoped store | `store.get(ws, id)` returns `None` for a foreign id; no unscoped accessor exists | `tenant-scoped-query-guard` | — | 🟡 core of isolation — agent-draft |
| T3 | Create + read project | `POST /projects` → 201 with a workspace-scoped row; `GET /projects/{id}` returns it; effect asserted | `structured-error-envelope`, `write-through-audit-log` | T1, T2 | 🟢 proven hooks, test-assertable, no boundary |
| T4 | List + cursor pagination | list returns only the caller's workspace; `limit` pages with a stable cursor over all rows once | `cursor-pagination`, `tenant-scoped-query-guard` | T1, T2 | 🟢 |
| T5 | Update project | `PATCH` mutates own row; foreign id → 404, cannot mutate | `tenant-scoped-query-guard`, `structured-error-envelope` | T3 | 🟢 |
| T6 | Delete project (admin) | admin `DELETE` → 204 + row gone; member → 403; foreign id → 404 before the role check | `rbac-check-at-boundary`, `tenant-scoped-query-guard` | T3 | 🔴 risk boundary (auth + isolation on a destructive verb) — human-owned |
| T7 | **Tenant isolation invariant** | one foreign id, every verb (GET/PATCH/DELETE) → 404; list never leaks; `CROSS_TENANT_DENIED` fires; 404 == pure-miss body | `tenant-scoped-query-guard`, `write-through-audit-log` | T3, T4, T5, T6 | 🔴 the core promise — human-certified, N-vote | 
| T8 | Denial observability | cross-tenant attempt emits `CROSS_TENANT_DENIED{workspace,target}`; member delete emits `RBAC_DENIED`; asserted from the trace | `write-through-audit-log` | T6, T7 | 🟢 |

> **Autonomy:** 🟢 agent-ship · 🟡 agent-draft · 🔴 human-only (risk boundary / out-of-repo dep).
> T6 + T7 are 🔴 by the profile rule — isolation is *the* risk boundary; an autonomous runner must
> not ship the core-promise authz slice unreviewed. They were human-certified (the isolation test +
> a 3-vote refutation, below).

## Build order

- **Waves:**
  - Wave 0 (no deps): T1, T2
  - Wave 1 (deps in W0): T3, T4
  - Wave 2: T5, T6
  - Wave 3: T7, T8
- **Critical path:** T2 → T3 → T6 → T7 (the isolation invariant depends on every verb existing).
- **Start now:** T1, T2 (graph-unblocked and un-gated).
- **Gated (not startable):** none — the token-issuer open question does not block verifying
  isolation against the dev stack (a test mints its own tokens).
