# Pump-station telemetry — Principles

> The values that bias every fork, before any rule. `edge-telemetry` profile.

## Universal

- **Grade the context, not just the code.** Every handoff passed a grader.
- **Author ≠ grader.** Nothing graded its own work.
- **No done without fresh evidence.** "Passes" = the fixture-replay + browser gate showed zero
  failures this session.
- **Fail loudly.** A silent wrong answer is worse than a loud stop.
- **Every correction given twice is a missing grader.**

## Domain values (`edge-telemetry`)

- **Missing data is a fact, not a gap — absence alerts.** A dropped or never-booted safety sensor
  raises CRITICAL; it is never read as "fine". This is the core promise.
- **A per-signal fault must not halt the whole station.** Severity is scoped per signal; one stale
  sensor doesn't blank the dashboard.
- **No bare thresholds.** Every level rule carries hysteresis; a raw `>` that can flap is wrong.
- **Severities are named constants**, never string literals — one source of truth, lint-enforced.
