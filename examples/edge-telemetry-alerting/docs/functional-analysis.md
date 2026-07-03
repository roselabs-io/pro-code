# Pump-station telemetry — Functional Analysis

> The behavioural spec. Frame's output, filled per the `edge-telemetry` profile.

## Identity

- **Product:** an industrial **pump-station telemetry monitor + alerting engine** with a served
  live dashboard.
- **Driver / owner:** the pro-code pipeline (regeneration run).
- **Primary goal:** never miss a safety-critical breach — every held bad value, and every dropped
  or dead-from-boot safety sensor, raises a CRITICAL alert; a nominal stream stays silent.

## Actors

| Actor | Role / privilege | Goals | Surfaces they touch |
|---|---|---|---|
| Operator | watches the station | see live signal status + active alerts at a glance | the dashboard |
| Edge device | streams readings | push sensor samples into the monitor | the ingest path |
| SRE / maintainer | tunes rules | adjust thresholds / TTLs without a code change | the station config (TOML) |

## Top-level workflows

- **Monitor a nominal station:** devices stream readings → the engine evaluates each against its
  rule → all in range → the dashboard shows every signal `ok`, no alerts.
- **A safety breach:** a signal crosses its limit and holds past debounce → the engine raises a
  CRITICAL alert (deduped) → the dashboard row turns red → the alert clears only when the value
  falls back past the hysteresis band.
- **A sensor drops / never boots:** a signal stops reporting (or never reports) past its TTL →
  the staleness watchdog raises a CRITICAL alert → the dashboard renders "— stale", never a number.

## Data model (business terms)

- **Device / signal** — a named sensor stream (discharge pressure, bearing temperature, flow rate),
  each with a unit, a safety-critical flag, and a rule.
- **Rule** — the alert condition for a signal: a threshold (with hysteresis + debounce) and/or a
  staleness TTL, plus a severity.
- **Alert** — a raised condition: signal, severity, kind (threshold | staleness), reason, count.
- **Reading** — one sample: signal, value, timestamp.

## Integrations

- **Device transport (inbound)** — edge devices push readings (`{signal, value, ts}`). In this
  slice the transport is a direct call / `POST /ingest`; a real deployment would front it with
  MQTT/HTTP. Contract: a reading is validated at ingest; a malformed line is rejected.
- **Notification delivery — OUT OF SCOPE.** The slice *raises* alerts; routing them to a channel
  (paging / email / MQTT) is explicitly not built here.

## Functionalities

- **F1 — Threshold alert** with hysteresis (fire past a limit; clear past limit ∓ h).
- **F2 — Debounce** — a breach must hold N consecutive samples (a single-sample spike is ignored).
- **F3 — Staleness watchdog** — absence within a TTL is an alert, including **dead-from-boot** (a
  sensor that never reported). *Safety-critical; the core promise.*
- **F4 — Alert dedup** — a burst of one condition is one active alert with an occurrence count.
- **F5 — Out-of-order tolerance** — a late earlier sample must not resurrect a cleared alert.
- **F6 — Severity tiering** — a breach maps to a named severity (`Severity.CRITICAL` / `WARNING`).
- **F7 — /state read model** — the current per-signal status + active alerts.
- **F8 — Live dashboard** — a served view that polls `/state` and renders status (stale/critical).
- **F9 — Alert observability** — every open/clear emits a structured event.

## Metrics + non-functionals

- **No missed critical alert (hard requirement)** — certified by fixture-replay (F3/F1 fire cases)
  + a nominal no-fire case. The core promise.
- **Accessibility** — dashboard status is not colour-only; a text label accompanies every row.
- **Observability** — `ALERT_RAISED{severity:critical}` / `ALERT_CLEARED` on every transition.

---
*Safety posture:* the two safety-critical signals (discharge pressure, bearing temperature) each
carry a threshold **and** a staleness rule at CRITICAL severity — the hard gate.
