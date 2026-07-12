# edge-telemetry-alerting — UI Sketches

> The user-facing surface, before any code. **Hard gate** for this profile — no handoff to Plan
> without this reviewed. Pulled from `doc-patterns/specs/ui-sketch.md`.

## View inventory

| View | Purpose |
|---|---|
| Station dashboard | the operator's one screen — every signal's live value + status, at a glance, refreshing on a poll |

## Wireframe per view

### Station dashboard

```
┌──────────────────────────────────────────────────────────┐
│  Station: pump-house-1            ● live   (updated 1s ago)│
├──────────────────────────────────────────────────────────┤
│  SIGNAL              VALUE        STATUS                    │
│  ─────────────────────────────────────────────────────    │
│  bearing_temp        73.2 °C      ● NOMINAL                 │
│  discharge_pressure  11.4 bar     ● CRITICAL  (overpressure)│
│  flow_rate           —  stale     ● WARNING   (— stale)     │
│  ─────────────────────────────────────────────────────    │
│  Active alerts: 2                                           │
└──────────────────────────────────────────────────────────┘
```

- **Shows:** one row per signal — name, value + unit (or "— stale" when stale), and a status cell carrying **both** a colour dot **and** a text label (NOMINAL / WARNING / CRITICAL / "— stale"). A footer counts active alerts. A "live" dot + "updated Ns ago" shows the poll is fresh.
- **Controls:** none — it's a read-only monitor. The view polls `/state` on an interval; there are no operator inputs in this slice.
- **Non-happy states:**
  - **Empty / boot:** a signal that has never reported renders "— stale" (safety-critical → CRITICAL), not a blank or a zero.
  - **Loading:** first paint before the first poll shows "…" placeholders, never a fabricated value.
  - **Error (monitor unreachable):** the "live" dot goes grey and a banner reads "monitor unreachable — values may be stale"; the last values grey out (never presented as fresh).
  - **Stale signal:** value cell shows **"— stale"** (never the last-good number), status shows the stale severity with its text label.

## Declined

- **Per-signal history / trend chart** — declined for the slice; the dashboard row (current value + status) is enough to prove the no-missed-alert promise. A trend view is a future feature.
- **Operator ack / silence controls** — declined; acking alerts is notification-delivery-adjacent (out of scope). The slice raises and displays, it doesn't manage.
- **Multi-station switcher** — declined; one station config for the slice.
