# {{project_name}} — Backlog

> The work Implement executes. One row per ticket, each **well-formed**: a verifiable
> acceptance criterion, a design hook (or explicit `novel`), `depends-on`, and an autonomy tier.
> The **starting** set — Implement adds rows as work surfaces them.
> Pulled from `doc-patterns/living-docs/backlog.md`.

## Tickets

| ID | Title | Acceptance criterion (verifiable) | Design hooks | Depends on | Autonomy |
|---|---|---|---|---|---|
| T1 | {TODO} | {TODO: an assertion the profile's grader can check — not "handle X well"} | {TODO: `hook.md` or `novel — author fresh`} | — | 🟢 {why} |
| T2 | {TODO} | {TODO} | {TODO} | T1 | 🟡 {why} |
| T3 | {TODO} | {TODO} | {TODO} | T1 | 🔴 {why} |

> **Acceptance criterion must be verifiable** in the profile's terms (e.g. `generic-saas`: an automated test can assert it). "Enforce isolation" is not a criterion; "cross-tenant GET returns 404, no other-tenant row ever serializes" is.
> **Autonomy:** 🟢 agent-ship · 🟡 agent-draft (agent scaffolds, human finishes) · 🔴 human-only (risk boundary or out-of-repo dependency). A prediction, re-confirmed at pickup.

## Build order

Derived from `depends-on` — no new input. **Fail loud on a cycle.**

- **Waves:**
  - Wave 0 (no deps): {TODO: T1, …}
  - Wave 1 (deps in Wave 0): {TODO: T2, …}
- **Critical path:** {TODO: the longest chain, e.g. T1 → T2 → T5 — drives the schedule}
- **Start now:** {TODO: graph-unblocked AND un-gated tickets}
- **Gated (not startable):** {TODO: ticket → the open question blocking it}
