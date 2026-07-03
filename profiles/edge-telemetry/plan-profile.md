# Profile — `edge-telemetry` · Plan

Domain: industrial edge telemetry monitoring + alerting. Pairs with this profile's `frame-profile.md`. Consumed by the unchanged `skills/plan` + `graders/plan-completeness`.

## Surface = a dashboard view

A "surface" here is a **monitoring view** the operator watches (not a CRUD page). Per-surface spec = one `docs/surfaces/<view>.md` per view in the UI sketch.

## Design catalog (the source of hooks)

The shapes Plan routes tickets against — **monitoring/edge patterns, nothing like the web-CRUD catalog.** Route ≤ 3–5 per ticket; no match → `novel — author fresh`.

| Shape | When it applies |
|---|---|
| `threshold-with-hysteresis` | fire when a signal crosses X, clear only when it falls back past X−h — so a value hovering at the line doesn't flap |
| `debounce-transient` | require the condition to hold for N samples / T seconds before firing — kills single-sample spikes |
| `staleness-watchdog` | absence of a reading within a TTL is itself an alert (usually critical) — missing ≠ nominal |
| `severity-tiering` | map a breach to a named severity; critical routes/escalates differently from warning |
| `alert-dedup-storm-guard` | collapse a burst of identical breaches into one active alert + an occurrence count |
| `rate-of-change-detector` | alert on slope, not level — a rapid rise that hasn't yet crossed the absolute threshold |
| `named-severity-constant` | any alert severity — `Severity.CRITICAL`, never the string `"critical"`; one source of truth, mechanically lint-enforced |
| `config-driven-thresholds` | any threshold / TTL / hysteresis band — lives in the station config, never a literal in the rule code (so re-tuning is a config edit, not a code change) |

## Out of scope — not ticketed

**Notification delivery** — routing a raised alert to a channel (paging / email / MQTT) — is out of scope: the slice *raises* alerts, it doesn't send them. Everything else the slice does — ingest, evaluation, the dashboard — is built and ticketed here.

## Tiering signals (what each rubric signal means here)

- **proven pattern** — a catalog shape above applies (not `novel`).
- **verifiable without a live device** — the rule is **replayable against a recorded fixture**; no hardware in the loop. *(In this domain the "verifiable without hardware" signal is literal, not a metaphor.)*
- **risk boundary** — a **safety-critical alert path**: a missed or wrong critical alert has a physical/safety consequence. This is the domain's core-promise boundary, the analogue of tenant isolation in `generic-saas`.
- **out-of-repo dependency** — lands in notification delivery or device firmware, outside this codebase.
- **spec-complete** — alert condition + severity defined + a dashboard sketch for any view in scope.

→ all-pass 🟢 · any-miss 🟡 · **safety-critical path or out-of-repo dependency 🔴**.

## Grader bar (consumed by `plan-completeness`)

- **`coverage_means`** — every alert condition in `functional-analysis.md` maps to ≥ 1 ticket, and **every safety-critical signal has a rule ticket**. A safety-critical signal is a functionality: it needs its own ticket, not a clause.
- **`verifiable_means`** — a fixture-replay asserts the alert, covering **both** a fire case and a no-fire case. "Alerts appropriately" fails the bar; "fixture `overpressure.jsonl` → one CRITICAL alert at t=14s; nominal fixture → zero alerts" passes.
- **well-formed bar:** each ticket carries a fixture-replay acceptance criterion + a catalog hook (or explicit `novel`) + wired `depends-on`; the backlog carries a cycle-free build order with the critical path called out.

## Notification routing (optional)

The canonical backlog is `docs/backlog.md`. Wiring alerts to real delivery channels (PagerDuty / email / MQTT topic) is an **optional profile add-on**, gated on the driver's OK (outward-facing). The pipeline is delivery-agnostic; the rule engine and its fixtures are the source of truth.
