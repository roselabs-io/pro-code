# edge-telemetry-alerting — Functional Analysis

> The behavioural spec: **what this system does**, in business terms. Not engineering.
> Pulled from `doc-patterns/specs/functional-analysis.md`; filled per the `edge-telemetry` profile.

## Identity

- **Product:** an industrial **edge telemetry monitor + alerting dashboard** — it ingests a station's sensor readings, evaluates alert rules, and shows each signal's live status to an operator.
- **Driver / owner:** plant SRE / control-room operator (clean-room build).
- **Primary goal:** **no missed critical alert** — every safety-critical breach (including a dropped/dead sensor) raises a CRITICAL alert; a stale signal renders "— stale", never a number or "nominal".

## Actors

| Actor | Role / privilege | Goals | Surfaces they touch |
|---|---|---|---|
| Operator | reads the dashboard | see live signal status; never miss a critical condition | the monitoring dashboard |
| Station / device | emits readings | stream telemetry into the monitor | device transport (ingest) |

## Top-level workflows

- **Ingest → evaluate → display:** the station streams readings → the monitor updates each signal's state, evaluating threshold (with hysteresis + debounce), staleness, and severity → alerts open/clear → the dashboard shows each signal's value + status, polling for updates.
- **Sensor goes dark:** a signal stops reporting → on read, its age exceeds the staleness TTL → it renders "— stale" and, if safety-critical, raises CRITICAL (a dropped sensor is a fact, not "fine"). A signal that never reported since boot ("dead from boot") is stale-critical too.

## Data model (business terms)

- **Station** — the monitored unit; owns a set of signals. Config-driven (`config/station.toml`).
- **Signal** — a measured channel: `name`, `unit`, `safety_critical` flag, and its rules. E.g. bearing temperature, discharge pressure, flow rate.
- **Rule** — an alert condition on a signal: a **level rule** (threshold + hysteresis + debounce, high or low direction, with warn/critical severities) and/or a **staleness rule** (a TTL past which absence alerts).
- **Alert** — an open condition on a signal: `signal`, `severity`, `opened_at`, an **occurrence count** (a burst dedups into one), and a cleared flag.

## Integrations

- **Device transport (ingest)** — inbound. Readings arrive as a stream of JSON lines `{signal, value, ts}` (a recorded fixture replays the same shape). One line each is parsed + validated at ingest; a malformed line is rejected.
- **Notification delivery — OUT OF SCOPE.** The slice *raises* alerts; routing them to a pager/email/MQTT channel is not built (profile-declared out of scope).

## Functionalities

- **Ingest a reading** — parse + validate a telemetry line; reject a malformed one.
- **Threshold alerting with hysteresis** — fire when a signal crosses a level; clear only when it falls back past the level by the hysteresis band, so a value hovering at the line doesn't flap.
- **Debounce transients** — require the condition to hold for N samples before firing; a single-sample spike doesn't alert.
- **Staleness watchdog** — absence of a reading within the TTL is itself an alert; for a safety-critical signal it's CRITICAL. Evaluated lazily on read (against the query clock), and from boot (a never-reported signal is stale).
- **Severity tiering** — a breach maps to a named severity (`Severity.CRITICAL` / `WARNING`); critical is the safety-critical path.
- **Alert dedup / storm guard** — a burst of the same breach is one active alert with an occurrence count, not N.
- **Out-of-order tolerance** — a late-arriving earlier sample must not resurrect a cleared alert.
- **The dashboard** — a served view + a `/state` endpoint; renders each signal's value + status, stale as "— stale", critical as red; polls for updates.

> Concrete signals + thresholds are a **build input the profile does not supply** (it gives the shapes, not the station's catalog). The chosen catalog is recorded in `docs/assumptions.md` as a flagged build assumption, not invented into this spec as settled fact.

## Metrics + non-functionals

- **No missed critical alert** — hard requirement; asserted by fixture-replay (fire + no-fire) + an adversarial N-vote.
- **Stale renders "— stale"** — the load-bearing visual invariant; asserted by the browser grader.
- **Observability** — every alert open/clear emits `ALERT_RAISED{signal,severity}` / `ALERT_CLEARED`.
- **Accessibility** — status is not colour-only; a text label accompanies the colour (browser grader checks the label).
