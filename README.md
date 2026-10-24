# pro-code

A pipeline for building software with coding agents. The name is the position: pro-code, not no-code — the pipeline assumes someone who understands the software stays in the loop, and gives agents a structure to work inside rather than replacing that person.

A runnable implementation of the ideas in [the article](https://blog.roselabs.io/posts/two-reading-journeys).

**Articles:** [Two reading journeys into agent engineering](https://blog.roselabs.io/posts/two-reading-journeys) · [The Map Around Claude Code](https://blog.roselabs.io/posts/the-map-around-claude-code) (part two).

Work moves through **Frame → Plan → Implement**; **Autopilot** runs Implement over a backlog. Each phase separates a *guide* (feedforward: domain-specific, supplied by a profile) from its *feedback* (agnostic). The pipeline ships the feedback and neutral guide skeletons; a **profile** fills the guides for a domain.

Two kinds of feedback ([`checks/README.md`](checks/README.md) defines them):

- **Checks** are deterministic: tools and scripts for lint, type, doctrine, security, tests, coverage, deps, logs, smoke, browser and infra. They run in a fixed order and stop at the first red.
- **The review** is LLM judgment: one session that did not write the diff reads it once, against one rubric ([`graders/review.md`](graders/review.md)). The **graders** under `graders/` (frame-, plan- and profile-completeness) are LLM judgment a person runs on demand.

## The pipeline

| Phase | Produces | Guide (from the profile) | Ends with |
|---|---|---|---|
| **Frame** | the spec — *what to build* | domain checklist + sources | the driver's sign-off |
| **Plan** | the backlog — *the work* | design catalog | the driver's sign-off |
| **Implement** | the code and the living docs | conventions · principles · CfRs | [review-gate](skills/review-gate/SKILL.md), then the human's acceptance |
| **Autopilot** | the run over the backlog | tiers + waves (from Plan) | one handoff for every dispatched ticket |

[review-gate](skills/review-gate/SKILL.md) runs on each ticket, in this order:

1. **Auto-fix arm** — formatters and the profile's codemods ([`codemods/`](codemods/README.md)).
2. **Checks** — the profile's `check-commands.md` rows in the order of [`checks/README.md`](checks/README.md#the-deterministic-tier-in-order), stopping at the first red. The author makes one fix attempt on a red check; a check still red after it stops the run with no review.
3. **One independent review** — a fresh session that did not write the diff applies the feature, drift, docs-currency and simplicity lenses of [`graders/review.md`](graders/review.md), then any lens unit the profile ships, and reports every finding in one pass.
4. **At most one fix pass** — the author addresses the findings once and the checks rerun. The review is not run again.
5. **Stop for the human** — the handoff lists the check results and each finding as fixed or open. The human accepts the ticket or reopens it.

### What runs automatically and what runs on demand

| What | When |
|---|---|
| auto-fix arm and checks | every ticket, before the review, and again after the fix pass |
| the review ([`graders/review.md`](graders/review.md)) | every ticket whose checks are green, once |
| the author's fix pass | when the review has findings; at most once |
| [frame-completeness](graders/frame-completeness.md) | on demand, before the driver signs off Frame |
| [plan-completeness](graders/plan-completeness.md) | on demand, before the driver signs off Plan |
| [profile-completeness](graders/profile-completeness.md) (GATE 0) | on demand, when a profile or overlay is written or changed |
| the evals ([`evals/`](evals/README.md)) | by hand, when a rubric changes; they call live models |

Nothing in the pipeline runs a grader between phases, runs graders in parallel on a ticket, reviews a ticket a second time, or loops until a grader passes.

## Changes from the multi-grader model

Until 2026-10 the pipeline ran a grader at each handoff: profile-completeness before Frame, frame-completeness at the end of Frame and plan-completeness at the end of Plan. Implement's gate ran about four graders in parallel (feature, drift, docs-currency, simplicity), each in its own session, then a fix pass and a re-grade for up to about three iterations, with an adversarial N-vote of several graders on the core promise.

| Earlier | Now |
|---|---|
| frame-, plan- and profile-completeness gate each handoff | the same graders, run on demand; each phase ends with the driver's sign-off |
| four graders in parallel, one session each | one review, one session, with the four as lenses of one rubric (`graders/review.md`; `graders/simplicity.md` became its simplicity lens) |
| fix pass → re-grade, up to ~3 iterations | at most one fix pass; the checks rerun; no second review |
| adversarial N-vote on the core promise | removed |
| profile-authored graders, budget of ~4 shared graders + 1 per overlay | profile-authored lens units of the one review; no grader budget |
| `graders/code-verification-loop.md`, a redirect to review-gate | deleted |

The measurement behind the change (pro-code evals, 2026-09-25): cost is turns × context; the graders are bound by their fixed context and the builders by their turns; and the frame and plan graders were `inert` in the eval cases — deleting the rule each case tested left the verdict unchanged ([`evals/README.md`](evals/README.md)). Governor, the dispatcher that runs agent work on this repository, adopted the resulting model: thin feedforward, deterministic checks, one independent review by a session other than the author, a bounded fix pass, and the human's product acceptance. Its harness posture records the reasons ([`harness-posture.md`](https://github.com/roselabs-io/governor/blob/main/governor/docs/postures/harness-posture.md), in a private repository).

## Layout

```
skills/frame|plan|implement/       the agnostic phase mechanisms (no domain content)
skills/review-gate/SKILL.md        Implement's gate: checks, one independent review, at most one fix pass
skills/autopilot/SKILL.md          orchestrator-workers — a worker per ticket across waves
doc-patterns/                      neutral doc skeletons, grouped by role (see doc-patterns/README.md):
  specs/                             what the pipeline produces — functional-analysis · ui-sketch · system-overview · surface-spec
  living-docs/                       memory kept current across the build — current-state · backlog · decision-record · assumptions
  guides/                            standing feedforward — principles · cfrs
  doctrines/                         enforced posture — comment-doctrine · test-posture · readme-doctrine
  harness/                           check + CLI scaffolding — log-taxonomy · justfile
codemods/README.md                 the deterministic auto-fix arm (stage 0 of review-gate)
checks/                            deterministic — README.md (the check/review/grader table + run order) ·
                                     coverage · dependencies · security · runtime-smoke ·
                                     browser (Playwright) · infra (build + boot) ·
                                     doctrine_lint.py (comment doctrine · test posture · forbids)
graders/                           LLM judgment — review (every ticket, once) · on demand:
                                     profile-completeness (GATE 0) · frame-completeness · plan-completeness
evals/                             mutation tests for the graders — README.md (the method) · build.py ·
                                     one case per rule shown to steer
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

Every directory under `examples/` is a service built end-to-end through the pipeline under one profile, gated green. The examples were built under the multi-grader model (*Changes from the multi-grader model* above); none has been rebuilt under the current review-gate. Each example's `docs/current-state.md` says what is built, what is not, and which checks the profile declares that the example has not wired.

- **[multi-tenant-isolation](examples/multi-tenant-isolation/)** (`generic-saas`, API): hard-done = *no cross-tenant leak*. Isolation is certified by an integration test and **held under a fresh adversarial refuter** (author ≠ grader) that attacked every verb — including a member cross-tenant delete (an existence oracle via RBAC ordering).
- **[edge-telemetry-alerting](examples/edge-telemetry-alerting/)** (`edge-telemetry`, UI): hard-done = *no missed critical alert*. Fixture-replay tests + real Playwright browser tests. Built via a **new profile with zero changes to any skill, check, or grader**. A sensor **dead from boot** (`decisions/0001`) raises CRITICAL.
- **[roselabs-blog](examples/roselabs-blog/)** (`saas-web`, full-stack + Compose): hard-done = *no draft or unpublished post readable by a public request*. Integration tests on a real Postgres, Playwright e2e on the live Compose stack, the infra check (fresh volume, migrations from empty). Added the `deploys` flag and the infra check as an additive extension.
- **[jay-z-projects](examples/jay-z-projects/)** (`generic-saas` + `personal/jay-z`): the same API as multi-tenant-isolation, built under a personal overlay — every comment carries the voice and stays doctrine-clean, checked by a profile-authored grader.

Structurally different domains — a CRUD API, a stream/rule engine, a full-stack deployed app — run through the **same skills, checks, and graders, byte-for-byte**; everything domain-specific lives in the swapped profile. In each, the tiering rubric refused to 🟢 agent-ship the core-promise tickets, and the gate — not author confidence — certified the hard-done.

[`COLD-REBUILD.md`](COLD-REBUILD.md) is the clean-room protocol: rebuild every example from the profile alone, in a fresh session, and promote any profile gap it surfaces. Examples #1, #2, and #4 have been through it; #3 (roselabs-blog) is in the protocol and has not yet been run.

Each mechanism the [article](https://blog.roselabs.io/posts/two-reading-journeys) describes shows up in at least one of the examples: codemods (a libcst transform), a logs check, a browser check (Playwright), an infra check (Compose from an empty volume), isolated review agents (author ≠ grader), orchestrator-workers, and an adversarial refutation that independently re-checked the core promise.
