# Profile — `edge-telemetry` · Frame

Domain: industrial **edge telemetry monitoring + alerting** (Python rule engine + a served dashboard). The second profile — the agnosticism proof. Nothing in `skills/` or `graders/` changes to support it; only this overlay differs from `generic-saas`.

## Sources (where Frame's context comes from)

| Source | Provides |
|---|---|
| Device / sensor spec sheet | the signals, their units, ranges, sample rates |
| Signal catalog / tag list | which signals exist and which are safety-critical |
| Ops runbook / incident history | the failures that have actually hurt — what *should* have alerted |
| SRE / operator interview *(brainstorm mode)* | thresholds, severities, escalation, when no brief exists |

## Functional-analysis sections

Same neutral template (`doc-patterns/specs/functional-analysis.md`), filled for this domain:
- **Required:** Identity · Actors · Top-level workflows · **Data model** = *devices · signals · rules · alerts* · Integrations = *device transport* · **Functionalities** = *the alert capabilities* · Metrics.
- **Optional (add only if they bite):** Out-of-scope, Compliance / safety posture.

List the *monitoring logic this product adds* — rule evaluation, staleness, alert tracking, the dashboard. Notification delivery (routing alerts to a channel) is out of scope.

## Hard gates

- **UI sketch** — the monitoring surface is user-facing, so no handoff to Plan without a reviewed `docs/ui-sketches.md` (view inventory + a wireframe per view + a declined list; template: `doc-patterns/specs/ui-sketch.md`). Missing/unreviewed = 🔴 blocking.
- **Alert-coverage of safety-critical signals** — *(domain-specific gate)* every signal marked **safety-critical** must have a defined **alert condition** (threshold and/or staleness) **and a severity** in the functional analysis. A safety-critical signal with no alert condition = 🔴 blocking — it's the domain's core promise, exactly as isolation is for `generic-saas`.

## Principles + CfRs (feedforward guides)

- **Principles** (`doc-patterns/guides/principles.md`): *missing data is a fact, not a gap — absence alerts*; *a per-signal fault must not halt the whole station* (severity scoping).
- **CfRs that bite** (`doc-patterns/guides/cfrs.md`): **Safety/Reliability** (no missed critical alert — hard, fixture-replay), **Observability** (every alert open/clear emits a structured event the logs grader reads), **Accessibility** (the dashboard's status is not colour-only — the browser grader checks the text label too).
- **`has_ui`:** true — the monitoring dashboard. The browser grader + UI-sketch gate are **live** for this profile.

## Grader bar (consumed by `frame-completeness`)

- **`verifiable_means`:** an alert rule can be **replayed against a recorded telemetry fixture** and its output asserted — *both* the fire case (a real breach → the alert) *and* the no-fire case (nominal data → silence). A rule you can't replay you can't grade.
- **`usual_silent_gaps`** — probe these; telemetry briefs routinely omit them:
  - **staleness** — missing data is not nominal data; a dropped sensor must alert, not read as "fine."
  - **flapping** — a value oscillating at the threshold; needs hysteresis, not a bare `>`.
  - **alert storms** — one fault emitting a burst; needs dedup / an active-alert count.
  - **clock skew / out-of-order readings** — a late-arriving earlier sample must not resurrect a cleared alert.
  - **0 vs null**, units / scaling — a raw count of 0 and "no reading" are different facts.
- **clean-handoff bar:** functional-analysis carries devices · signals catalog · alert conditions (with severity) · device integration · metrics; open-questions logs every biting assumption; UI sketch reviewed; **every safety-critical signal has an alert condition** (the hard gate).
