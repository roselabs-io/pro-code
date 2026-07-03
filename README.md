# pro-code

Coding is getting commoditized, and with it a wave of hype: vibe coding, low-code, no-code — the promise that you won't really need to write software anymore. This isn't about that. Real software still needs someone who understands it — hence the name: pro-code, not no-code. Keep that person in the loop, and let agents amplify them.

A small, self-contained pipeline for building software with coding agents — a concrete, runnable implementation of the ideas discussed in [the article](https://roselabs-io.github.io/pro-code/two-reading-journeys.html).

The shape: build in phases — **Frame → Plan → Implement** (run at scale by **Autopilot**) — and make each handoff pass a **grader** before the next phase starts.

> **Each phase separates a _guide_ (feedforward — domain-specific, swappable) from a _grader_ (feedback — agnostic).**
> The pipeline ships the graders + neutral guide skeletons; a **profile** fills the guides for a domain.

A phase produces its output, then a grader checks it before the handoff — that gate is what makes an autonomous loop worth trusting. It's one concrete take on the feedforward/feedback split the [article](https://roselabs-io.github.io/pro-code/two-reading-journeys.html) describes, not a framework.

## The pipeline

| Phase | Produces | Guide (swappable) | Grader (agnostic) |
|---|---|---|---|
| **Frame** | the spec — *what to build* | domain checklist + sources | **frame-completeness** — ✅ |
| **Plan** | the decomposition — *the work* | design catalog | **plan-completeness** — ✅ |
| **Implement** | the code | conventions · principles · CfRs | **code-verification-loop** — ✅ |
| **Autopilot** | the run — *build the backlog* | tiers + waves (from Plan) | dispatches the loop per ticket — ✅ |

The **code-verification-loop** is the keystone: an auto-fix arm (codemods) → deterministic graders (type · lint · test · **logs** · **browser**) → ~3 **isolated** fuzzy graders (feature · drift · docs), fix-once-and-re-grade, with an adversarial **N-vote** on the core promise. Author ≠ grader throughout.

The first grader is the highest-leverage one: **errors at Frame compound through every downstream step**, so the ask→Frame handoff is where a completeness gate pays the most. That's why Frame ships first.

## Layout

```
skills/frame|plan|implement/       the agnostic phase mechanisms (no domain content)
skills/autopilot/SKILL.md          orchestrator-workers — fan out a worker per ticket across waves
doc-patterns/                      neutral doc skeletons, grouped by role (see doc-patterns/README.md):
  specs/                             what the pipeline produces — functional-analysis · ui-sketch · system-overview · surface-spec
  living-docs/                       memory kept current across the build — current-state · backlog · decision-record · assumptions
  guides/                            standing feedforward — principles · cfrs
  doctrines/                         enforced posture — comment-doctrine · test-posture · readme-doctrine
  harness/                           grader + CLI scaffolding — log-taxonomy · justfile
codemods/README.md                 the deterministic auto-fix arm (stage 0 of the loop)
graders/frame-completeness.md      Frame grader (the done-signal ceremony)
graders/plan-completeness.md       Plan grader (coverage gate + well-formedness)
graders/code-verification-loop.md  the keystone — auto-fix · deterministic graders · isolated fuzzy graders · N-vote
graders/browser-grader.md          Playwright — grade the running UI (what the user sees)
graders/checks/doctrine_lint.py    special-lint grader — comment doctrine · test posture · domain forbids
profiles/                          the guide/grader seam — domain overlays
  generic-saas/                    default profile — web CRUD SaaS  (built example #1)
  edge-telemetry/                  second profile — industrial alerting  (built example #2)
examples/
  multi-tenant-isolation/          #1 — API slice, hard-done = no cross-tenant leak
  edge-telemetry-alerting/         #2 — UI slice, hard-done = no missed critical alert
```

> The files under `skills/` and `graders/` are shared **byte-for-byte** by both domains. Everything domain-specific lives in the swapped `profiles/<domain>/` — that separation is the point.

## Status

The pipeline runs end-to-end twice — two example services, each gated green.

- **[Example #1 — multi-tenant-isolation](examples/multi-tenant-isolation/)** (`generic-saas`, API): hard-done = *no cross-tenant leak*. 27 tests. Isolation is certified by an integration test and **held under a fresh adversarial refuter** (author ≠ grader) that attacked every verb — including a member cross-tenant delete (an existence oracle via RBAC ordering).
- **[Example #2 — edge-telemetry-alerting](examples/edge-telemetry-alerting/)** (`edge-telemetry`, UI): hard-done = *no missed critical alert*. 28 fixture-replay tests + 2 real Playwright browser tests. Built via a **new profile with zero changes to any skill or grader**. Every safety-critical breach — including a sensor **dead from boot** (`decisions/0001`) — raises CRITICAL; certified by fixture-replay and **held under a fresh adversarial refuter**.

Two structurally-opposite domains — a CRUD API and a stream/rule engine — run through the **same skills and graders, byte-for-byte**; everything domain-specific lives in the swapped profile. In both, the tiering rubric refused to 🟢 agent-ship the core-promise tickets, and the grader — not author confidence — certified the hard-done.

Each mechanism the [article](https://roselabs-io.github.io/pro-code/two-reading-journeys.html) describes shows up in at least one of the examples: codemods (a libcst transform), a logs grader, a browser grader (Playwright), isolated review agents (author ≠ grader), orchestrator-workers, and an adversarial refutation that independently re-checked the core promise.
