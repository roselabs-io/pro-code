# {{project_name}} — System Overview

> The 30,000-foot picture: the system's shape, its dataflows, its boundaries.
> A new dev reads this first to orient. Keep it ≤ 200 lines — detail lives per-surface.
> Pulled from `doc-patterns/specs/system-overview.md`; filled per the active profile from the functional analysis.

## Components

The system's main parts, one line each. External services this talks to go under **Integration boundaries** below — list here only what this project builds.

| Component | What it does |
|---|---|
| {TODO: e.g., Tenant-scoping middleware} | {TODO} |

## Key dataflows

From the functional-analysis workflows. One sequenced narrative per top-level flow.

- {TODO: "Actor does X → backend does Y → surface shows Z → actor confirms → …"}

## Integration boundaries

One paragraph per external system — **every entry from the functional analysis's Integrations section gets covered here**, with a contract sketch (protocol · trigger · payload). If a contract is unclear, log an open question instead of inventing it.

- {TODO: e.g., Payment provider — outbound REST; we call on checkout; inbound webhook `charge.succeeded` → {payload sketch}}

## Tech-stack call-outs

Only what diverges from the profile's defaults, with the reason.

- {TODO: e.g., "Postgres row-level security instead of app-layer scoping — isolation is the core promise, defense-in-depth wanted."}

---
*Optional — add only if it bites: **Cross-cutting posture** (a security / compliance / performance stance the whole system must hold, when there's an explicit requirement).*
