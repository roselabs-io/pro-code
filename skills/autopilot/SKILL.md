---
name: autopilot
description: "Phase 3 runner — the orchestrator-workers pattern. Decompose Plan's backlog into independent chains, fan out a worker sub-agent per ticket across the dependency waves, run each through the verification loop with isolated graders, and aggregate one residual handoff."
---

# Autopilot (the orchestrator-workers runner)

Autopilot is how **Implement scales past one ticket at a time.** Where `implement` builds a single ticket with the driver in the loop, autopilot is the **lead** that reads Plan's backlog, **fans out a worker per ticket** across the parallelizable waves, and **aggregates** the results into one honest handoff. It's the **orchestrator-workers** pattern, made concrete over a real backlog.

Autopilot **writes no code itself.** It decomposes, dispatches, routes by tier, collects, and reports. The workers write code; the graders judge it; autopilot is the conductor.

Domain-neutral by design. *What* the tickets are, *what* the graders check, *what* a tier means come from Plan's output + the active profile. This skill is the **orchestration mechanism**.

## What it consumes

- `docs/backlog.md` — the tickets, their `depends-on`, and the **autonomy tiers** (🟢/🟡/🔴) + the **build order** (waves + critical path). Plan already computed all of it; autopilot executes it.
- The active profile — the verification-loop roster (deterministic checks, fuzzy rubrics, graders) each worker's output is graded against.

## The loop

```
read backlog → compute the attemptable set (tier ∩ graph-unblocked ∩ un-gated)
   → for each wave, IN PARALLEL:
        dispatch a worker sub-agent per ticket  ──┐
        each worker: author → verification loop   │  (fresh context per worker)
        graders run as ISOLATED sub-agents        │  (author ≠ grader)
   → collect per-ticket results ←──────────────────┘
   → advance to the next wave (deps now landed)
   → aggregate → ONE residual handoff
```

## Routing by tier (the orchestrator's dispatch rule)

Plan predicted a tier per ticket; autopilot routes on it:

- **🟢 agent-ship** — dispatch a worker for the full build; it runs to green through the verification loop.
- **🟡 agent-draft** — dispatch a worker to *scaffold*; hand the half-done work to the human to finish + verify. Marked draft in the handoff.
- **🔴 human-only** — **do not dispatch.** Skip to the handoff as human-owned work. The core-promise / boundary tickets stay with a person by design.

**Attemptability is live, not the tier.** A ticket is dispatched only when it's tier-eligible **and** graph-unblocked **and** un-gated by an open question — recomputed each wave, not read once.

## Two rules that keep it honest

- **Pickup re-check (the runtime tier confirmation).** Before a worker commits to a 🟢/🟡 ticket, it reads the real context and **bails to the handoff if reality contradicts the tier** — a ticket that looked shippable but touches a boundary the spec missed is escalated, not forced. Plan predicts; the worker confirms; the verify gate arbitrates.
- **Isolated graders (author ≠ grader, enforced).** A worker never grades its own output. Autopilot runs the fuzzy graders as **separate sub-agents with fresh context** — the generative/adversarial split made structural.

## Parallelization — waves, not a free-for-all

Autopilot fans out **within a wave** (tickets whose deps have all landed) and barriers **between waves** (a wave can't start until its dependencies merged). This is **parallelization (sectioning)**: independent tickets build concurrently; dependent ones wait. The critical path Plan flagged is the wall-clock floor.

Optionally, on the **core-promise finding**, run an **adversarial N-vote verify** — several isolated graders each try to *refute* that the promise holds; it survives only on a majority. Reserve it for the one invariant that must not be wrong (isolation; no-missed-alert).

## The handoff is the residual, not the whole

Autopilot ends with **one aggregated report**, not N piles of diff:

- 🟢 **shipped** — ticket green through the loop; nothing for the human but a glance.
- 🟡 **drafted** — scaffolded; the human finishes the flagged part.
- 🔴 **human-only** — never attempted; owned by a person.
- ⚠️ **escalated** — a worker bailed at pickup, or the loop stalled (same finding recurred). A stall is signal — the hard thing worth attention.

The human reviews the 🟡 + 🔴 + ⚠️ residual, not the 🟢 the graders already cleared. **That** is what removes the human as the bottleneck.

## Stopping conditions

- All attemptable tickets resolved (shipped / drafted / escalated) → handoff.
- A worker's loop hits max-iterations or stalls → escalate that ticket, keep the others going.
- A wave produces a dependency surprise (a ticket reveals a new blocker) → re-plan that sub-tree; don't force a garbage order.

## What autopilot does NOT do

- **Write code** — the workers do.
- **Grade** — the isolated grader sub-agents do.
- **Re-tier** — that's a Plan re-run on a planning change; autopilot only recomputes *attemptability*.
- **Ship 🔴** — ever. Boundary / core-promise work is human-owned.
