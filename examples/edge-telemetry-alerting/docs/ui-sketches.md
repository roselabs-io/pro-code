# Pump-station telemetry — UI Sketches

> The user-facing surface, before code. Required hard gate for this UI-bearing profile.

## View inventory

| View | Purpose |
|---|---|
| Station dashboard | the operator watches every signal's live status + the active alerts, at a glance |

## Wireframe per view

### Station dashboard

```
┌────────────────────────────────────────────────────────────┐
│  Pump-station telemetry            ● live                    │
├──────────────────────┬─────────────────┬───────────────────┤
│  Signal              │  Reading        │  Status           │
├──────────────────────┼─────────────────┼───────────────────┤
│  discharge_pressure  │  11.6 bar       │  CRITICAL   (red) │
│  bearing_temperature │  — stale        │  STALE · CRITICAL │
│  flow_rate           │  42 m3ph        │  ok               │
├──────────────────────┴─────────────────┴───────────────────┤
│  Active alerts                                              │
│   [critical] discharge_pressure 11.5bar crossed 10.0 (×2)  │
│   [critical] bearing_temperature stale — never reported…   │
└────────────────────────────────────────────────────────────┘
```

- **Shows:** one row per signal (name · reading · status) + an active-alert list. State comes from
  `GET /state`, polled every 2s.
- **Controls:** none — it's a read-only monitor (no operator actions in this slice).
- **Non-happy states:**
  - **Stale:** the reading cell renders **"— stale"**, never a number; the row is red if
    safety-critical (`visual_invariant`).
  - **Critical breach:** the row renders **red**; the reading shows the breaching number.
  - **Unreachable:** the live-dot goes grey and the label reads "unreachable" if `/state` fails.

## Declined

- **Per-signal history / trend charts** — declined for the slice; the live row + alert list is
  enough to prove the monitor. A real product would add sparklines.
- **Operator actions (ack / silence an alert)** — declined; the slice raises alerts, it doesn't
  manage their lifecycle (that pairs with notification delivery, which is out of scope).
