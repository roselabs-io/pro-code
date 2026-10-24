---
name: "autopilot"
description: "Phase 3 runner — the orchestrator-workers pattern. Decompose Plan's backlog into dependency waves, dispatch a worker per ticket, run each through review-gate (checks, one independent review, at most one fix pass), and aggregate one handoff for the human."
consumed_by: ["orchestrator"]
canonical_for: "running the phases unattended"
profile: agnostic
---

# Autopilot (the orchestrator-workers runner)

Autopilot runs Implement over more than one ticket. Where `implement` builds a single ticket with the
driver in the loop, autopilot reads Plan's backlog, dispatches a worker per ticket across the
dependency waves, and aggregates the results into one handoff.

Autopilot writes no code. It decomposes, dispatches, routes by tier, collects and reports. Workers
write code; a separate review session reads each diff.

*What* the tickets are, *what* the review checks and *what* a tier means come from Plan's output and
the active profile. This skill is the orchestration mechanism.

## What it consumes

- `docs/backlog.md` — the tickets, their `depends-on`, the **autonomy tiers** (🟢/🟡/🔴) and the
  **build order** (waves and critical path) Plan computed.
- The active profile (resolved per [`profiles/CONTRACT.md#active-profile-resolution`](../../profiles/CONTRACT.md#active-profile-resolution)) — the check commands and review rubrics
  [`skills/review-gate`](../review-gate/SKILL.md) applies to each worker's diff.

## The run

```
read backlog → compute the attemptable set (tier ∩ graph-unblocked ∩ un-gated)
   → for each wave, in parallel:
        a worker per ticket (fresh context)       ──┐
        each worker: author → review-gate           │  checks → one review → ≤ 1 fix pass
        the review runs in its own session          │  (author ≠ reviewer)
   → collect per-ticket results ←────────────────────┘
   → advance to the next wave (deps now landed)
   → aggregate → one handoff
```

## Routing by tier

Plan predicted a tier per ticket; autopilot routes on it:

- **🟢 agent-ship** — dispatch a worker for the full build through review-gate.
- **🟡 agent-draft** — dispatch a worker to scaffold; the human finishes and verifies. Marked draft in
  the handoff.
- **🔴 human-only** — not dispatched. Listed in the handoff as human-owned work.

A ticket is dispatched only when it is tier-eligible, graph-unblocked and not gated by an open
question — recomputed each wave.

## Rules

- **Pickup re-check.** Before a worker commits to a 🟢/🟡 ticket, it reads the real context and returns
  the ticket to the handoff if the context contradicts the tier (a ticket that touches a boundary the
  spec missed is escalated, not forced).
- **Author ≠ reviewer.** A worker never reviews its own diff. Autopilot starts the review as a separate
  session with fresh context.
- **One review, one fix pass per ticket.** Autopilot does not rerun the review after the fix pass.

## Parallelization — waves

Autopilot dispatches within a wave (tickets whose dependencies have all landed) and waits between waves.
The critical path Plan flagged is the wall-clock floor.

## The handoff

Autopilot ends with one aggregated report:

- 🟢 **shipped** — checks green; the review's findings each fixed or listed open.
- 🟡 **drafted** — scaffolded; the human finishes the flagged part.
- 🔴 **human-only** — not attempted.
- ⚠️ **escalated** — the worker bailed at pickup, a check is still red after the attempt before the
  review (no review ran), or a check is still red after the fix pass.

Every ticket goes to the human for acceptance. The report puts open findings, red checks, 🟡, 🔴 and ⚠️
first.

## Stopping conditions

- Every attemptable ticket resolved (shipped, drafted or escalated) → handoff.
- A check still red after a worker's attempt before the review → that ticket is escalated without a
  review; the others continue.
- A check still red after a worker's fix pass → that ticket is escalated; the others continue.
- A wave reveals a new dependency → re-plan that sub-tree; the wave order is not forced.

## What autopilot does NOT do

- **Write code** — the workers do.
- **Review** — a separate review session does.
- **Re-tier** — that is a Plan re-run; autopilot only recomputes attemptability.
- **Dispatch 🔴** — boundary and core-promise work is human-owned.
