# pro-code

A pipeline for building software with coding agents. The name is the position: pro-code, not no-code — the pipeline assumes someone who understands the software stays in the loop, and gives agents a structure to work inside rather than replacing that person.

A runnable implementation of the ideas in [the article](https://roselabs-io.github.io/pro-code/two-reading-journeys.html).

**Articles:** [Two reading journeys into agent engineering](https://roselabs-io.github.io/pro-code/two-reading-journeys.html) · [The Map Around Claude Code](https://roselabs-io.github.io/pro-code/the-map-around-claude-code.html) (part two).

Work moves through **Frame → Plan → Implement**, run at scale by **Autopilot**. Each handoff has to pass a gate before the next phase starts.

> **Each phase separates a _guide_ (feedforward — domain-specific, swappable) from its gate (feedback — agnostic).**
> The pipeline ships the gates and neutral guide skeletons; a **profile** fills the guides for a domain.

Two kinds of gate, and the distinction is load-bearing ([`checks/README.md`](checks/README.md) defines it):

- **Checks** are deterministic — tools and scripts. Lint, type, doctrine, security, tests, coverage, deps, logs, smoke, browser, infra. Cheap, reproducible, and they short-circuit. A check that passes is proof.
- **Graders** are LLM judgment — completeness, drift, docs-currency, simplicity. Expensive, run as isolated sub-agents with fresh context, author ≠ grader enforced. A grader that passes is an opinion, which is why they vote.

## The pipeline

| Phase | Produces | Guide (swappable) | Gate (agnostic) |
|---|---|---|---|
| **Frame** | the spec — *what to build* | domain checklist + sources | **frame-completeness** |
| **Plan** | the decomposition — *the work* | design catalog | **plan-completeness** |
| **Implement** | the code | conventions · principles · CfRs | **review-gate** — the code-verification loop |
| **Autopilot** | the run — *build the backlog* | tiers + waves (from Plan) | dispatches review-gate per ticket |

**review-gate** is the Implement gate: an auto-fix arm (codemods) → the checks, in a fixed order → ~4 isolated graders (feature · drift · docs · simplicity), fix once, re-grade, with an adversarial N-vote on the core promise. A **GATE 0** (profile-completeness) runs once before Frame and checks the profile itself.

Frame ships first because errors in the spec compound through every downstream phase, so the ask→Frame handoff is where a completeness gate pays most.

## Layout

```
skills/frame|plan|implement/       the agnostic phase mechanisms (no domain content)
skills/review-gate/SKILL.md        the code-verification loop — Implement's gate (orchestrates checks + graders)
skills/autopilot/SKILL.md          orchestrator-workers — fan out a worker per ticket across waves
doc-patterns/                      neutral doc skeletons, grouped by role (see doc-patterns/README.md):
  specs/                             what the pipeline produces — functional-analysis · ui-sketch · system-overview · surface-spec
  living-docs/                       memory kept current across the build — current-state · backlog · decision-record · assumptions
  guides/                            standing feedforward — principles · cfrs
  doctrines/                         enforced posture — comment-doctrine · test-posture · readme-doctrine
  harness/                           check + CLI scaffolding — log-taxonomy · justfile
codemods/README.md                 the deterministic auto-fix arm (stage 0 of the loop)
checks/                            deterministic — README.md (the check/grader table + run order) ·
                                     coverage · dependencies · security · runtime-smoke ·
                                     browser (Playwright) · infra (build + boot) ·
                                     doctrine_lint.py (comment doctrine · test posture · forbids)
graders/                           LLM judgment — profile-completeness (GATE 0) · frame-completeness ·
                                     plan-completeness · simplicity
profiles/                          the guide/gate seam — domain overlays (CONTRACT.md is the hook list)
  generic-saas/                    API-only Python SaaS
  edge-telemetry/                  industrial telemetry + alerting, with a dashboard
  saas-web/                        full-stack web SaaS, deployed via Compose
  personal/jay-z/                  a personal overlay — additive-only
examples/                          one built service per profile (+ one per overlay); each README names its
                                     profile, its hard-done, and how to run it
```

> The files under `skills/`, `checks/` and `graders/` are shared **byte-for-byte** by every domain. Everything domain-specific lives in the swapped `profiles/<domain>/`, selected per project by its `.pipeline-profile` file.

## Status

Every directory under `examples/` is a service built end-to-end through the pipeline under one profile, gated green. Each example's `docs/current-state.md` says what is built, what is not, and which checks the profile declares that the example has not wired.

- **[multi-tenant-isolation](examples/multi-tenant-isolation/)** (`generic-saas`, API): hard-done = *no cross-tenant leak*. Isolation is certified by an integration test and **held under a fresh adversarial refuter** (author ≠ grader) that attacked every verb — including a member cross-tenant delete (an existence oracle via RBAC ordering).
- **[edge-telemetry-alerting](examples/edge-telemetry-alerting/)** (`edge-telemetry`, UI): hard-done = *no missed critical alert*. Fixture-replay tests + real Playwright browser tests. Built via a **new profile with zero changes to any skill, check, or grader**. A sensor **dead from boot** (`decisions/0001`) raises CRITICAL.
- **[roselabs-blog](examples/roselabs-blog/)** (`saas-web`, full-stack + Compose): hard-done = *no draft or unpublished post readable by a public request*. Integration tests on a real Postgres, Playwright e2e on the live Compose stack, the infra check (fresh volume, migrations from empty). Added the `deploys` flag and the infra check as an additive extension.
- **[jay-z-projects](examples/jay-z-projects/)** (`generic-saas` + `personal/jay-z`): the same API as multi-tenant-isolation, built under a personal overlay — every comment carries the voice and stays doctrine-clean, checked by a profile-authored grader.

Structurally different domains — a CRUD API, a stream/rule engine, a full-stack deployed app — run through the **same skills, checks, and graders, byte-for-byte**; everything domain-specific lives in the swapped profile. In each, the tiering rubric refused to 🟢 agent-ship the core-promise tickets, and the gate — not author confidence — certified the hard-done.

[`COLD-REBUILD.md`](COLD-REBUILD.md) is the clean-room protocol: rebuild every example from the profile alone, in a fresh session, and promote any profile gap it surfaces. Examples #1, #2, and #4 have been through it; #3 (roselabs-blog) is in the protocol and has not yet been run.

Each mechanism the [article](https://roselabs-io.github.io/pro-code/two-reading-journeys.html) describes shows up in at least one of the examples: codemods (a libcst transform), a logs check, a browser check (Playwright), an infra check (Compose from an empty volume), isolated review agents (author ≠ grader), orchestrator-workers, and an adversarial refutation that independently re-checked the core promise.
