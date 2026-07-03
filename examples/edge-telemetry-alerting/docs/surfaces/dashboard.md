# Station dashboard — Surface Spec

> Surface = a monitoring view (`edge-telemetry`: a surface is a dashboard view).

## What it does

- **Purpose:** let an operator see every signal's live status + the active alerts at a glance.
- **Actors:** operator (read-only).
- **Shows / returns:** one row per signal (name · reading · status) and an active-alert list,
  driven by `GET /state`, polled every 2s.

## Controls / inputs

| Control / input | Triggers | Notes |
|---|---|---|
| (auto-poll) | `GET /state` every 2s | no operator actions in this slice |

## Calls + contracts

- `GET /state` → `{station, signals: [{name, unit, value, stale, status, safety_critical, ts}],
  alerts: [{signal, severity, kind, reason, count}], generated_at}`.
- `POST /ingest {signal, value, ts}` → `202` (edge devices push readings).

## States

- **Nominal:** every row `ok`, empty alert list.
- **Critical breach:** the row renders **red**; the reading cell shows the breaching number;
  the alert appears in the list.
- **Stale (incl. dead-from-boot):** the reading cell renders **"— stale"** (never a number);
  the row is red for a safety-critical signal (`visual_invariant`).
- **Unreachable:** the live-dot goes grey, label "unreachable" if `/state` fails.

## Design shapes referenced

- `threshold-with-hysteresis` · `debounce-transient` · `staleness-watchdog` ·
  `alert-dedup-storm-guard` · `named-severity-constant` · `config-driven-thresholds`.
