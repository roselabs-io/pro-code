# Profiles — the guide/gate seam

A **profile** is the domain overlay. The pipeline ships agnostic **checks** + **graders** + neutral **guide skeletons**; a profile fills the guides and supplies the check commands and grader rubrics for one domain. **Swap the profile, retarget the whole pipeline** — this is what makes pro-code agnostic.

pro-code draws this boundary explicitly: the *mechanism* (how a phase runs) and the *content* (what it asks about) stay separate, not tangled in one skill.

## What a profile supplies

For **Frame**:
- **sources** — where upstream context comes from in this domain (a SaaS brief + tickets; an industrial sales kickoff + transcripts; a research question + papers).
- **sections** — which functional-analysis sections are required vs optional here.
- **hard gates** — phase-specific blockers (`generic-saas`: a reviewed UI sketch for any user-facing app).
- **grader bar** — `verifiable_means`, `usual_silent_gaps`, the clean-handoff bar (consumed by [`graders/frame-completeness.md`](../graders/frame-completeness.md)).

For **Plan** a profile also supplies the **design catalog** (the shapes tickets route against) and the **tiering signals**; for **Implement**, the **check commands**, the grader **rubrics**, and the domain **false-green traps**. Same hook *shape* every skill, check, and grader reads; entirely different *content* per domain. The exhaustive list is [`CONTRACT.md`](CONTRACT.md); the check-vs-grader split is defined in [`../checks/README.md`](../checks/README.md).

**Which profile is active** is resolved per run from `$PROFILE` or the project's `.pipeline-profile` file ([`CONTRACT.md#active-profile-resolution`](CONTRACT.md#active-profile-resolution)). There is no default.

## Profiles

- **`generic-saas/`** — A Python + FastAPI CRUD API (API-only). Frame + Plan + Implement. Built [example #1](../examples/multi-tenant-isolation/) and, with the `personal/jay-z` overlay, [example #4](../examples/jay-z-projects/).
- **`edge-telemetry/`** — industrial telemetry monitoring + alerting (Python engine + served dashboard). Frame + Plan + Implement. Built [example #2](../examples/edge-telemetry-alerting/).
- **`saas-web/`** — full-stack web SaaS: **FastAPI (async) + React/TS/MUI + async Postgres**, deployed via Docker Compose (`deploys: true`). Frame + Plan + Implement. Adds a rendered frontend *and* a graded deploy dimension (the additive [infra check](../checks/infra.md)) on top of the `generic-saas` API baseline. Built [example #3](../examples/roselabs-blog/).
- **`local-app/`** — a local desktop application around a model pipeline: **Python stage functions + local models + one remote model API + a `pywebview` window**, `deploys: false`. Adds a domain grader unit (`graders/boundary.md`: nothing of the user's leaves the machine unredacted) and the `gate-before-egress` / `synthetic-fixture-with-key` / `examples-as-template` shapes. Built [example #4](../examples/praxis/).
- *(add your own — a research profile, a compiler profile — by copying a profile dir and swapping the content. The skills, checks, and graders don't change.)*

> **Agnostic is a design property, proven by a _second_ profile — and it now is.** `edge-telemetry` dropped in with **zero changes to any skill, check, or grader** (audited: nothing under `skills/`, `checks/`, or `graders/` was touched); `saas-web` then added the `deploys` flag + infra check additively. The one addition to the shared layer was a *neutral* guide skeleton — `doc-patterns/specs/ui-sketch.md` — that the UI-sketch hard gate references but the API-only #1 never exercised. Mechanism and feedback are shared byte-for-byte; only the profile content differs.
