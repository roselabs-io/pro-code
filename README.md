# pro-code

*Not no-code. Pro-code, agent-amplified.* An agnostic **harness + pipeline** for building software with agents — the unit of production is **expert + agent**.

pro-code is a software-building pipeline — **Frame → Plan → Implement**, run at scale by **Autopilot** — where each phase is a handoff **gated by a grader**. It's built around one commitment:

> **Every phase separates a _guide_ (feedforward — domain-specific, swappable) from a _grader_ (feedback — agnostic, universal).**
> The pipeline ships the **graders** + neutral **guide skeletons**; a **profile** fills the guides for your domain.

pro-code **leads with the graders**: each phase produces its output, then a grader checks it before the handoff. That gate is what makes an autonomous loop trustworthy.

It is a full **harness** in Böckeler's sense (all 12 guide + grader sub-elements) and covers all **5 of Anthropic's agent patterns** — audited in [COVERAGE.md](COVERAGE.md).

The two bodies of work behind it — Böckeler's harness engineering and Anthropic's agent posts — are mapped in [two-reading-journeys.md](two-reading-journeys.md).

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
COVERAGE.md                        full Böckeler + Anthropic coverage audit
```

> The files under `skills/` and `graders/` are shared **byte-for-byte** by both domains. Everything domain-specific lives in the swapped `profiles/<domain>/`. That's the whole thesis, made literal.

## Status

**The pipeline is complete, runs end-to-end twice, and covers Böckeler's full harness + Anthropic's 5 patterns** ([COVERAGE.md](COVERAGE.md)).

- **[Example #1 — multi-tenant-isolation](examples/multi-tenant-isolation/)** (`generic-saas`, API): hard-done = *no cross-tenant leak*. 25 tests. The loop caught a real cross-tenant write-leak; an isolated drift grader caught worker over-commenting; a 3-vote refutation on isolation held 3/3.
- **[Example #2 — edge-telemetry-alerting](examples/edge-telemetry-alerting/)** (`edge-telemetry`, UI): hard-done = *no missed critical alert*. 27 tests + a real Playwright browser grader. Built via a **new profile with zero changes to any skill or grader** (audited). A 3-vote refutation **found a genuine missed-critical bug** (a sensor dead from boot) that the tests were green over — the loop closed it (`decisions/0001`).

Two structurally-opposite domains — a CRUD API and a stream/rule engine — run through the **same skills and graders, byte-for-byte**. Everything domain-specific lives in the swapped profile. In both, the tiering rubric refused to 🟢 agent-ship the core-promise tickets, and the grader — not author confidence — certified the hard-done.

**Full coverage, demonstrated in runnable examples.** Böckeler's 12 sub-elements + Anthropic's 5 patterns, each first-class in the plugin and exercised in an example: codemods (a libcst transform), logs grader, browser grader (Playwright), isolated review-agents (author ≠ grader), orchestrator-workers (real parallel worker sub-agents), and the adversarial N-vote, which caught a real bug in each example. See [COVERAGE.md](COVERAGE.md).
