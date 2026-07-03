---
name: plan
description: "Phase 2 — transform the reviewed spec (functional-analysis + open-questions) into the work: a system overview, per-surface specs, and a sequenced, tiered backlog of well-formed tickets that Implement can execute."
---

# Plan (phase 2 — the work)

Plan turns the **reviewed spec** Frame produced into **the work** Implement executes: a high-level system view, a spec per surface, and a backlog of tickets — sequenced into a build order and tiered for autonomy. It's the bridge between *what to build* and *building it*, and it **closes with a grader** — [`graders/plan-completeness.md`](../../graders/plan-completeness.md) — before anything hands off.

**Frame's opposite.** Frame was human dialogue — pattern-*less*, mostly *in* the loop. Plan is an agent **transform** (frame docs → tickets) — pattern-*rich*, mostly *on* the loop: the agent decomposes and sequences, you review and own the two judgment calls (architecture, tiering). De-black-boxed, Plan is exactly three things: **a chain, two routings, and an exit grader.**

Plan is **domain-neutral by design.** *What* design shapes exist to route against and *what* a "surface" even is come from a **profile** (`profiles/<domain>/`), not from this skill. This skill is the **mechanism**; the profile is the **content**. Default profile: `generic-saas`.

## What you read

- `docs/functional-analysis.md` and `docs/open-questions.md` — Frame's output. **If required sections are missing, push back to Frame — don't guess.**
- `open-questions.md`'s **Design seeds → Plan** bucket — design ideas Frame parked. Treat each as a **hypothesis, not a decision**: read the relevant catalog entry fresh, then confirm or reject. Never adopt a seed just because it's written down.
- The profile's **design catalog** — the shapes you route tickets against (below).

## The chain (the spine)

Each step consumes the previous. Don't skip forward — a backlog drafted before the system view is a backlog of guesses.

```
functional-analysis → system-overview → per-surface specs → backlog → sequencing
```

1. **System overview** (`docs/system-overview.md`) — the 30,000-foot picture, pulled from [`doc-patterns/specs/system-overview.md`](../../doc-patterns/specs/system-overview.md): the system's main components and, from the functional analysis, every integration boundary with a contract sketch.
2. **Per-surface specs** (`docs/surfaces/<name>.md`) — one drill-down per surface the profile declares (a UI page, an API endpoint, a job — the profile names what a "surface" is). Pulled from [`doc-patterns/specs/surface-spec.md`](../../doc-patterns/specs/surface-spec.md): what it shows/does, controls/inputs, the calls it makes + contracts, the non-happy states, the design shapes it references. Sketch-shaped — **Implement fills the detail.**
3. **Backlog** (`docs/backlog.md`) — one ticket per functionality (at minimum), each **well-formed**: a *verifiable* acceptance criterion, a design hook (or an explicit `novel`), and `depends-on`. Pulled from [`doc-patterns/living-docs/backlog.md`](../../doc-patterns/living-docs/backlog.md).
4. **Sequencing** — derived, not authored (below).

## The two routings

Both run per-ticket, inside the backlog step.

- **Design-hook matching.** For each ticket, scoop **≤ 3–5** relevant shapes from the profile's catalog and cite them in the ticket's hooks. No clean match → write `novel — author fresh` and flag it, so a shape worth promoting gets caught later. The catalog shape is the *reusable* pattern; the surface spec is *this project's* adaptation of it.
- **Autonomy tiering 🟢🟡🔴.** Predict how far each ticket can go autonomously, so Implement's runner can filter on it. A fixed yes/no rubric — **the shape is agnostic; the profile defines what each signal *means* in this domain:**
  - proven pattern (a real catalog hook, not `novel`)?
  - verifiable without a human in the loop (a test / mock confirms it)?
  - touches a risk boundary (auth, isolation, an external contract, anything security- or safety-critical)?
  - depends on something outside this codebase you don't control (another service, party, or system)?
  - spec-complete (acceptance criterion + surface spec where there's a surface)?

  → 🟢 **agent-ship** (all pass) · 🟡 **agent-draft** (any miss — agent scaffolds, human finishes) · 🔴 **human-only** (a risk-boundary or out-of-repo-dependency hit — hard 🔴 regardless of the rest). One-line *why* per tier.

**The tier is a prediction, not a guarantee** — Implement's runner re-confirms it at pickup and the verify gate arbitrates. And **Plan still produces no code** — it only predicts.

## Sequencing — pure derivation

No new planning input; turn the `depends-on` edges into an order.

- **Waves** — Wave 0 = no deps; each later wave = tickets whose deps all landed earlier. Waves expose the parallelizable work.
- **Critical path** — the longest dependency chain. Flag every ticket on it — it drives the schedule.
- **Cycle-check** — a cycle in `depends-on` is a **fail-loud**: name the offending tickets, emit no order.
- **Graph-unblocked ≠ startable.** A ticket with no deps can still be **gated by an open question**. Keep the two distinct; a ticket is "start now" only when it's both graph-unblocked **and** un-gated.

Write a **Build order** section into `docs/backlog.md`: the waves, the critical chain, the start-now set.

## The discipline

- **Concrete, not abstract.** Plan *this* project, not software in general.
- **Sketch-shaped.** Specs are drill-downs for Implement to fill, not final designs. Keep them tight.
- **Seeds are hypotheses.** Read the catalog entry fresh; confirm or reject — never rubber-stamp a parked seed.
- **No code.** If you catch yourself writing an implementation, stop — it's a ticket, not a diff.

## Park what spills

Mid-plan you'll surface things that aren't this phase's artifacts. **Grasp → categorize → route** — don't bury them in `system-overview` or backlog prose.

- a functional gap / the spec is wrong → a surprises log, and **push the fix back to Frame**.
- a knowingly-cut corner → a tech-debt log.
- a non-trivial decision + why → a decisions / ADR log.
- a future feature beyond this build → the backlog, flagged out-of-scope-for-now.

## Close — run the completeness grader

Plan **doesn't trail off.** Before handoff, run the plan-completeness ceremony ([`graders/plan-completeness.md`](../../graders/plan-completeness.md)): a **coverage** map (every functionality → ≥1 ticket), a 🟢/🟡/🔴 well-formedness scorecard framed by *implement-time cost*, a tiering + sequencing sanity pass, and an explicit two-path sign-off. The ceremony is agnostic; the **profile supplies the bar** — what "covered," "verifiable," and "well-formed" mean in this domain. It's a **fresh grader** — author ≠ grader, so the plan gets adversarial eyes before Implement eats it.

## What you do NOT produce

- **Code** — that's Implement.
- **`functional-analysis.md` content** — that's Frame.
- **A frozen architecture** — the specs and backlog are *living docs*; Implement updates them when reality surprises the plan.

## What you DO push back on

- **Frame underweight** — "I can't draft the system view without the integration contracts; send it back to Frame."
- **Catalog gap** — "No shape covers X; Implement authors it fresh — flag it for promotion once it stabilizes."
- **Speculative requirements** — if the functional analysis waves its hands ("the system picks the right one"), don't launder that into a ticket's acceptance criterion. Push back.
