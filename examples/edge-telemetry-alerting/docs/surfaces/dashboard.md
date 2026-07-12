# dashboard — Surface Spec

> One drill-down per surface — here a "surface" is the **monitoring view** the operator watches.
> Pulled from `doc-patterns/specs/surface-spec.md`.

## What it does

- **Purpose:** show every signal's live value + status so the operator never misses a critical condition.
- **Actors:** operator (read-only).
- **Shows / returns:** per signal — name, value + unit (or "— stale"), a severity + text label, a colour dot; a footer active-alert count; a live/updated indicator. Driven by `GET /state`.

## Controls / inputs

| Control / input | Triggers | Notes / validation |
|---|---|---|
| (auto-poll) | `GET /state` every N seconds | read-only; no operator inputs in this slice |

## Calls + contracts

- `GET /state` → `200 { station, now, signals: [ { name, unit, value: number|null, stale: bool, severity: "info"|"warning"|"critical", label: string } ], active_alerts: int }`
  - a **stale** signal serializes `value: null, stale: true, label: "— stale"` (never a last-good number).
  - severity is the enum's string value; the client maps CRITICAL → red, and always renders the `label` text (not colour-only).

## States

- **Empty / boot:** a never-reported signal → `value:null, stale:true`; safety-critical → `severity:"critical"`.
- **Loading:** first paint before the first poll → "…" placeholders, no fabricated values.
- **Error (monitor unreachable):** live dot greys, "monitor unreachable" banner, last values greyed (not fresh).
- **Stale:** value cell shows "— stale"; status shows the stale severity + label.

## Design shapes referenced

- `staleness-watchdog` — absence within TTL → alert; safety-critical → CRITICAL; rendered "— stale".
- `severity-tiering` + `named-severity-constant` — status maps to a named severity constant.
- `threshold-with-hysteresis`, `debounce-transient`, `alert-dedup-storm-guard` — drive the severity the row shows.
- `config-driven-thresholds` — the limits behind the status come from `station.toml`.
