# Profile — `generic-saas` · Plan

Domain: a CRUD SaaS backend — **Python + FastAPI, API-only**. The **default** profile. Pairs with `frame-profile.md`.

## Surface = an API endpoint group

A "surface" in this domain is a **group of related API endpoints** (e.g. the projects endpoints). Per-surface spec = one `docs/surfaces/<name>.md` per endpoint group. (For a UI profile, "surface" would instead mean a page or view — that's the swap; see `edge-telemetry`.)

## Design catalog (the source of hooks)

The shapes Plan routes tickets against. A small, isolation-centered set — enough to prove hook-routing, not a framework. Route ≤ 3–5 per ticket; no match → `novel — author fresh`.

| Shape | When it applies |
|---|---|
| `tenant-scoped-query-guard` | any read/write that must never cross a tenant boundary — scope every query by tenant, deny-by-default |
| `rbac-check-at-boundary` | an action gated by role — enforce at the request boundary, not in the caller |
| `severity-tiered-validation` | request input with mixed warn/block rules — tier the validation, gate the write on blocking-clean |
| `cursor-pagination` | any list that can grow unbounded — stable cursor paging, not offset |
| `idempotent-webhook-handler` | an inbound webhook that may redeliver — dedupe on event id, safe to replay |
| `structured-error-envelope` | any failure response — a typed `{status, code, detail}`, never a bare 500 or a leaked stack; the status is chosen (404 vs 403) deliberately |
| `write-through-audit-log` | any state mutation — emit a structured **log event** (a stable event code) *as* the write lands, so the logs grader can prove the handler ran (ties to the Observability CfR) |

*(Add shapes as real builds surface them; flag `novel` tickets for promotion once they stabilize.)*

## Tiering signals (what each rubric signal means here)

- **proven pattern** — a catalog hook above applies (not `novel`).
- **verifiable without a human in the loop** — an automated test can assert the criterion (unit / integration / e2e) against the dev stack or a mock; the bar is "a test, not a person, confirms it."
- **risk boundary** — touches **auth, tenant isolation, or an external contract** (a webhook/payment/email integration). Isolation is *the* boundary in this profile.
- **out-of-repo dependency** — needs a change outside this codebase you don't control.
- **spec-complete** — acceptance criterion present + a surface spec exists for any endpoint group in scope.

→ all-pass 🟢 · any-miss 🟡 · risk-boundary or out-of-repo dependency 🔴.

## Grader bar (consumed by `plan-completeness`)

- **`coverage_means`** — every functionality in `functional-analysis.md` maps to ≥ 1 ticket whose acceptance criterion, if it passes, delivers that functionality. Isolation is a functionality: it needs its own ticket, not a clause.
- **`verifiable_means`** — an automated test can assert the acceptance criterion. "Handle X properly" / "enforce Y" fail the bar; a concrete assertion (status code, serialized shape, a row that must/mustn't exist) passes.
- **well-formed bar:** each ticket carries a test-assertable criterion + a catalog hook (or explicit `novel`) + wired `depends-on`; the backlog carries a cycle-free build order with the critical path called out.

## External tracker sync (optional)

The canonical backlog is `docs/backlog.md`. Mirroring rows to an external tracker (Jira / Linear / GitHub Issues) — and wiring `depends-on` as blocker links — is an **optional profile add-on**, gated on the driver's OK (shared-tracker writes are outward-facing). The pipeline mechanism is tracker-agnostic; the doc is the source of truth.
