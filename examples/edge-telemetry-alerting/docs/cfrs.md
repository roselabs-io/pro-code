# edge-telemetry-alerting — Cross-Functional Requirements (CfRs)

> The "-ilities", named so they're gradeable. Pulled from `doc-patterns/guides/cfrs.md`;
> the `edge-telemetry` profile declares which bite.

## The -ilities

| CfR | Bites? | The bar (verifiable) | Graded by |
|---|---|---|---|
| Security | baseline | a malformed ingest line is rejected, not trusted | ingest test |
| Reliability / Safety | **bites** | no missed critical alert — every safety-critical breach (incl. dead/stale sensor) → CRITICAL; fixture-replay fire + no-fire | fixture-replay tests + N-vote |
| Performance | n/a | — (single-station reference slice) | — |
| Observability | **bites** | every alert open/clear emits `ALERT_RAISED{signal,severity}` / `ALERT_CLEARED` | logs grader |
| Accessibility | **bites** | dashboard status is not colour-only — a text label accompanies the colour; stale renders "— stale" | browser grader |
| Scalability | baseline | out-of-order tolerant; dedup collapses a storm to one alert | dedup/order tests |
| Maintainability | **bites** | lint + comment-doctrine clean; severities are named constants (no string literals); thresholds config-driven | ruff · doctrine_lint · special-lint |

> Three biting CfRs carry concrete, test-assertable bars: Safety (fixture-replay), Observability (logs grader), Accessibility (browser grader). Each maps to a grader — no biting CfR is left unverifiable.
