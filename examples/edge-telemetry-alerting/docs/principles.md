# edge-telemetry-alerting — Principles

> Feedforward values that bias every decision. Pulled from `doc-patterns/guides/principles.md`;
> domain values from the `edge-telemetry` profile.

## Universal (hold in every domain)

- **Grade the context, not just the code.** Every handoff passes a grader before the next phase eats it.
- **Author ≠ grader.** Nothing grades its own work; a fresh critic has fresh priors.
- **No done without fresh evidence.** "Should pass" is not "passed this session."
- **Fail loudly.** A silent wrong answer is worse than a loud stop.
- **Every correction given twice is a missing grader.** Encode the rubric; don't re-nag.

## Domain values (from `edge-telemetry`)

- **Missing data is a fact, not a gap — absence alerts.** A dropped sensor is stale-critical, never read as "fine" or a last-good number.
- **A per-signal fault must not halt the whole station.** Severity is scoped per signal; one bad channel doesn't blind the others.
- **Never miss a critical.** When in doubt at a fork, bias toward raising — a false CRITICAL is cheap next to a missed one.
