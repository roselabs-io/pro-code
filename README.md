# pro-code

A pipeline for building software with coding agents. The name is the position: pro-code, not no-code — the pipeline assumes someone who understands the software stays in the loop, and gives agents a structure to work inside rather than replacing that person.

A runnable implementation of the ideas in [the article](https://roselabs-io.github.io/pro-code/two-reading-journeys.html).

**Articles:** [Two reading journeys into agent engineering](https://roselabs-io.github.io/pro-code/two-reading-journeys.html) · [The Map Around Claude Code](https://roselabs-io.github.io/pro-code/the-map-around-claude-code.html) (part two).

Work moves through **Frame → Plan → Implement**, run at scale by **Autopilot**. Each handoff has to pass a gate before the next phase starts.

> **Each phase separates a _guide_ (feedforward — domain-specific, swappable) from its gate (feedback — agnostic).**
> The pipeline ships the gates and neutral guide skeletons; a **profile** fills the guides for a domain.

Two kinds of gate, and the distinction is load-bearing:

- **Checks** are deterministic — tools and scripts. Type, lint, test, coverage, dependencies, security, logs, browser, infra. Cheap, reproducible, and they short-circuit. A check that passes is proof.
- **Graders** are LLM judgment — completeness, drift, docs-currency. Expensive, run as isolated sub-agents with fresh context, author ≠ grader enforced. A grader that passes is an opinion, which is why they vote.

## The pipeline

| Phase | Produces | Guide (swappable) | Gate (agnostic) |
|---|---|---|---|
| **Frame** | the spec — *what to build* | domain checklist + sources | **frame-completeness** — ✅ |
| **Plan** | the decomposition — *the work* | design catalog | **plan-completeness** — ✅ |
| **Implement** | the code | conventions · principles · CfRs | **code-verification-loop** — ✅ |
| **Autopilot** | the run — *build the backlog* | tiers + waves (from Plan) | dispatches the loop per ticket — ✅ |

The **code-verification-loop** is the Implement gate: an auto-fix arm (codemods) → checks (type · lint · test · logs · browser) → ~3 isolated graders (feature · drift · docs), fix once, re-grade, with an adversarial N-vote on the core promise.

Frame ships first because errors in the spec compound through every downstream phase, so the ask→Frame handoff is where a completeness gate pays most.

## Layout

```
skills/frame|plan|implement/       the agnostic phase mechanisms (no domain content)
skills/autopilot/SKILL.md          orchestrator-workers — fan out a worker per ticket across waves
doc-patterns/                      neutral doc skeletons, grouped by role (see doc-patterns/README.md):
  specs/                             what the pipeline produces — functional-analysis · ui-sketch · system-overview · surface-spec
  living-docs/                       memory kept current across the build — current-state · backlog · decision-record · assumptions
  guides/                            standing feedforward — principles · cfrs
  doctrines/                         enforced posture — comment-doctrine · test-posture · readme-doctrine
  harness/                           gate + CLI scaffolding — log-taxonomy · justfile
codemods/README.md                 the deterministic auto-fix arm (stage 0 of the loop)
graders/                           LLM judgment — frame-completeness · plan-completeness ·
                                     profile-completeness · code-verification-loop
checks/                            deterministic — coverage · dependencies · security ·
                                     browser (Playwright) · infra (build + boot) ·
                                     doctrine_lint.py (comment doctrine · test posture · forbids)
profiles/                          the guide/gate seam — domain overlays
  generic-saas/                    default profile — web CRUD SaaS  (built example #1)
  edge-telemetry/                  second profile — industrial alerting  (built example #2)
examples/
  multi-tenant-isolation/          #1 — API slice, hard-done = no cross-tenant leak
  edge-telemetry-alerting/         #2 — UI slice, hard-done = no missed critical alert
```

> The files under `skills/`, `graders/` and `checks/` are shared **byte-for-byte** by both domains. Everything domain-specific lives in the swapped `profiles/<domain>/`.

## Status

The pipeline runs end-to-end twice — two example services, each gated green.

- **[Example #1 — multi-tenant-isolation](examples/multi-tenant-isolation/)** (`generic-saas`, API): hard-done = *no cross-tenant leak*. 27 tests. Isolation is certified by an integration test and **held under a fresh adversarial refuter** (author ≠ grader) that attacked every verb — including a member cross-tenant delete (an existence oracle via RBAC ordering).
- **[Example #2 — edge-telemetry-alerting](examples/edge-telemetry-alerting/)** (`edge-telemetry`, UI): hard-done = *no missed critical alert*. 28 fixture-replay tests + 2 real Playwright browser tests. Built via a **new profile with zero changes to any skill or grader**. Every safety-critical breach — including a sensor **dead from boot** (`decisions/0001`) — raises CRITICAL; certified by fixture-replay and **held under a fresh adversarial refuter**.

Two structurally-opposite domains — a CRUD API and a stream/rule engine — run through the **same skills and graders, byte-for-byte**; everything domain-specific lives in the swapped profile. In both, the tiering rubric refused to 🟢 agent-ship the core-promise tickets, and the grader — not author confidence — certified the hard-done.

Each mechanism the [article](https://roselabs-io.github.io/pro-code/two-reading-journeys.html) describes shows up in at least one of the examples: codemods (a libcst transform), a logs check, a browser check (Playwright), isolated review agents (author ≠ grader), orchestrator-workers, and an adversarial refutation that independently re-checked the core promise.
