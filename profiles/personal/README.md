---
consumed_by: ["orchestrator"]
canonical_for: "how a personal overlay composes"
profile: personal
---

# Personal profiles — reviewing taste, layered on

A **personal profile** is a lean overlay that composes *on top of* the active domain profile
(`generic-saas`, `edge-telemetry`, …). It's how an individual holds their own work to a bit more than the
shared bar, without touching anyone else's rules. See [`../CONTRACT.md`](../CONTRACT.md) → *Two kinds*.

## Add yours
1. Copy `../_skeleton/personal-profile.md` → `personal/<name>/personal-profile.md`.
2. Fill only what you want: extra drift-rubric rows, extra `doctrine_lint` forbids, or your own grader
   units in `personal/<name>/graders/` (copy `../_skeleton/grader.md`).
3. The loop composes it: **agnostic graders + the domain profile + your overlay.**

## The one rule: additive-only
An overlay can **only tighten** — add checks, never relax or remove a domain/agnostic rule. GATE-0 flags
any overlay that tries to weaken the gate.

## Budget
A personal **check** (a `--forbid` row) is free. A personal **grader** rides as a +1 above the shared ~4
grader budget (agnostic + domain) — add one only if it earns its place. See `../../checks/README.md`.

*No personal profiles are committed — this is the ready-to-use home.*
