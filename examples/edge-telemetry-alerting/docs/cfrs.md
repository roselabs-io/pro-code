# Pump-station telemetry — Cross-Functional Requirements

> The -ilities, named so they're gradeable. A biting CfR with no verifiable bar is a 🔴 for the plan grader.

| CfR | Bites? | The bar (verifiable) | Graded by |
|---|---|---|---|
| Safety / Reliability | **bites** | no missed critical alert — every safety-critical breach (held value, stale, dead-from-boot) → CRITICAL; nominal → silent; fixture-replay | `test_no_missed_critical.py` + N-vote |
| Observability | **bites** | every alert open/clear emits a structured event; `ALERT_RAISED{severity:critical}` on a breach | logs grader (`test_logs_grader.py`) |
| Accessibility | **bites** | dashboard status is not colour-only — a text label accompanies every row; a stale row reads "— stale" | browser grader (`test_dashboard_browser.py`) |
| Performance | baseline | in-memory engine; no latency target set for the slice | — |
| Maintainability | **bites** | ruff clean (E,F,I,B); comment-doctrine clean; severity is an enum constant (special-lint) | ruff + doctrine_lint |
| Scalability | n/a | single-station slice | — |
| Security | n/a | no auth surface in the monitor slice | — |

> The four biting CfRs — Safety, Observability, Accessibility, Maintainability — each map to a
> running check, so none is a hand-wave. Safety and Accessibility are the two the browser + fixture
> graders certify that unit tests alone could not.
