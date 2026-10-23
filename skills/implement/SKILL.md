---
name: "implement"
description: "Phase 3 — build a ticket: author the code and the living docs, then run review-gate: the checks, one independent review (author ≠ reviewer) and at most one fix pass, ending in a handoff to the human."
consumed_by: ["build"]
canonical_for: "the Implement phase mechanism"
profile: agnostic
---

# Implement (phase 3 — build, then review)

Implement turns a **well-formed ticket** from Plan's backlog into **working, reviewed code**. The phase is *produce the code, then gate it*: the checks, then one independent review, then the human.

Implement is **domain-neutral by design.** *What* commands prove it runs, *what* conventions the review's drift lens reads, *what* the false-green traps are — all come from a **profile** (`profiles/<domain>/`), not this skill. This skill is the **mechanism**; the profile is the **content**. The active profile is resolved per run from `$PROFILE` or the project's `.pipeline-profile` ([`profiles/CONTRACT.md#active-profile-resolution`](../../profiles/CONTRACT.md#active-profile-resolution)); there is no default.

## One phase, three beats

**author → verify → review.** Verify is the checks; review is one independent review in a fresh session. Both are run by [`skills/review-gate`](../review-gate/SKILL.md). This skill drives the beats; that skill specifies the sequence.

**One ticket or the whole backlog.** This skill is *ticket-scoped* — the driver pulls one ticket and works it with you. To run the backlog at scale — dispatch a worker per ticket across the dependency waves, each diff reviewed by a separate session — use [`skills/autopilot`](../autopilot/SKILL.md) (the orchestrator-workers runner). Autopilot dispatches; `implement` is what each worker runs.

## Guides you run (deterministic)

Author *with* the feedforward tools, not just against the docs:
- **Language server (LSP)** — consult defs/refs/types (pyright/mypy/tsc) *before* editing, not just to type-check after. Semantic facts beat guessing a signature.
- **CLIs / scripts** — one entry point per action (`just up/down/test/lint/typecheck/fix/gate`; template: [`doc-patterns/harness/justfile`](../../doc-patterns/harness/justfile)). review-gate's checks and you invoke the *same* commands.
- **Codemods** — when a convention spans N files, a script enforces it ([`codemods/`](../../codemods/README.md)); review-gate runs the auto-fix arm before a check reports mechanical drift.

## What you read at ticket start

Per ticket, in order — and if any is missing, **push back to Plan before writing code, don't guess**:

1. **The ticket** — acceptance criterion, design hooks, `depends-on` (from Plan's backlog).
2. **The surface spec** (`docs/surfaces/<name>.md`) for any surface the ticket touches.
3. **The design shapes** named in the ticket's hooks — read the profile's catalog entry (and any reference it points to) **fresh**. Never copy; adapt the shape to *this* code.
4. **The system overview** if the ticket crosses an integration boundary.
5. **The living docs** — `current-state.md`, the decisions log, `open-questions.md` — surface prior decisions and open gates relevant to this ticket.

## How a ticket goes

1. **Read the context** (above).
2. **Sketch the change** — out loud: "We're adding X, shaped by `<hook>`, touching these files. Anything missing?" Don't code yet.
3. **Author** — code shaped to the design hook. The catalog is the *shape*; this code is the *adaptation*.
4. **Verify + review** — hand the diff to [review-gate](../review-gate/SKILL.md): the checks in order, then one independent review, then at most one fix pass with the checks rerun.
5. **Maintain the living docs** — your second job (below).
6. **Hand off** — the check results and each review finding, fixed or open, for the human's acceptance.

One ticket at a time.

## No "done" without fresh evidence

**If you didn't run it this session, you can't say it passes** — say what you actually did instead. "Tests pass" means the test command's output showed zero failures, now — not "should pass." Confidence is not evidence. If verification failed or you couldn't run it, *that's* the status you report; don't dress it up. This is the discipline the verify gate enforces mechanically — but it holds even when you're driving by hand.

## Living docs — your second job (the second artifact)

A run produces **two artifacts, not one: the code *and* the context.** The code is what runs; the markdowns are what the *next agent knows*. **Stale docs don't just fail to help — they poison the next run** (the next agent reads them as truth and drifts worse). So maintaining the docs *is* maintaining the memory — and the review's **docs-currency lens** reads it like code.

Update these *as you write the code*, never as a retrofit:

- **`docs/backlog.md`** — shipped items **deleted** (git is the record); new work this ticket surfaced **added**. Forward-only — the rule agents always violate.
- **`docs/current-state.md`** — reflects what's *now* built. The doc a fresh agent reads first.
- **`docs/open-questions.md`** — questions this ticket resolved flipped to `[decided]`; new assumptions logged `[open]`.
- **The decisions log** — a decision record for any non-obvious call (a reversed approach, a chosen alternative, a new convention). The *why* the next reader can't re-derive from the diff. Skip the obvious; skip "used hook X" (that's the ticket's hook).
- **The surface spec** — updated if reality diverged from Plan's sketch.

## Park what spills

Implement is the pipeline's main **spill producer** — reality bites here. **Grasp → categorize → route**, then keep building:

- a wrong assumption / the spec is wrong → a surprises log, and **push the fix back to Frame or Plan**.
- a knowingly-cut corner → a tech-debt log.
- a non-trivial decision + why → the decisions log.
- a future feature → the backlog, flagged out-of-scope-for-now.

## What you do NOT do

- **Don't claim done without the verify gate.** Code changed ≠ criterion met. Run it.
- **Don't redesign silently.** If the hooks don't fit reality, log a surprise, update the spec, *then* code differently. Silent divergence is the failure mode.
- **Don't copy from another project.** The catalog shape is the source of truth; adapt, don't lift.
- **Don't review your own work.** The review runs in a **fresh session** — author ≠ reviewer. Self-review is lenient and blind to its own assumptions.
- **Don't write tests "later."** If the area calls for tests, they're part of *this* ticket.

## Close — review-gate, not a self-review

Implement closes by running the code through [review-gate](../review-gate/SKILL.md) and handing off the check results and each review finding, marked fixed or open. The human accepts the ticket or reopens it.
