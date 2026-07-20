# Profiles — the guide/grader seam

A **profile** is the domain overlay. The pipeline ships agnostic **graders** + neutral **guide skeletons**; a profile fills the guides and tunes the graders for one domain. **Swap the profile, retarget the whole pipeline** — this is what makes pro-code agnostic.

pro-code draws this boundary explicitly: the *mechanism* (how a phase runs) and the *content* (what it asks about) stay separate, not tangled in one skill.

## What a profile supplies

For **Frame**:
- **sources** — where upstream context comes from in this domain (a SaaS brief + tickets; an industrial sales kickoff + transcripts; a research question + papers).
- **sections** — which functional-analysis sections are required vs optional here.
- **hard gates** — phase-specific blockers (`generic-saas`: a reviewed UI sketch for any user-facing app).
- **grader bar** — `verifiable_means`, `usual_silent_gaps`, the clean-handoff bar (consumed by [`graders/frame-completeness.md`](../graders/frame-completeness.md)).

For **Plan** a profile also supplies the **design catalog** (the shapes tickets route against) and the **tiering signals**; for **Implement**, the **deterministic-check commands**, the fuzzy-grader **rubrics**, and the domain **false-green traps**. Same hook *shape* every skill and grader reads; entirely different *content* per domain.

## Profiles

- **`generic-saas/`** — the default. A Python + FastAPI CRUD API (API-only). Frame + Plan + Implement. Built [example #1](../examples/multi-tenant-isolation/).
- **`edge-telemetry/`** — industrial telemetry monitoring + alerting (Python engine + served dashboard). Frame + Plan + Implement. Built [example #2](../examples/edge-telemetry-alerting/).
- **`saas-web/`** — full-stack web SaaS: **FastAPI (async) + React/TS/MUI + async Postgres**, deployed via Docker Compose (`deploys: true`). Frame + Plan + Implement. Adds a rendered frontend *and* a graded deploy dimension (the additive [infra grader](../graders/infra-grader.md)) on top of the `generic-saas` API baseline. First example: the roselabs blog.
- *(add your own — a research profile, a compiler profile — by copying a profile dir and swapping the content. The skills and graders don't change.)*

> **Agnostic is a design property, proven by a _second_ profile — and it now is.** `edge-telemetry` dropped in with **zero changes to any skill or grader** (audited: nothing under `skills/` or `graders/` was touched). The one addition to the shared layer was a *neutral* guide skeleton — `doc-patterns/specs/ui-sketch.md` — that the UI-sketch hard gate references but the API-only #1 never exercised. Mechanism and feedback are shared byte-for-byte; only the profile content differs.
