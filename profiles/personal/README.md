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
Deterministic personal graders are free. **Fuzzy** ones count against the shared ~3 fuzzy budget
(agnostic + domain + personal) — add one only if it earns its place.

*No personal profiles are committed — this is the ready-to-use home.*
