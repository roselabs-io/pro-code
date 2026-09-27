---
consumed_by: [grader:simplicity]
canonical_for: the over-building rubric
profile: agnostic
---

# Grader — simplicity (over-building)

Checks that the diff builds **what the ticket asked for and nothing else**. The other graders look for
what is missing or wrong; this one looks for what is *extra*. An agent's default is to generalize — an
abstraction for the one call site, a config knob nobody set, an interface with one implementation, an
endpoint the spec never named, a "while I'm here" refactor of neighbouring code. Each is unreviewed
surface that the next ticket inherits.

Agnostic: the *lens* lives here; the ticket's acceptance criterion, design hooks, and the profile's
declared choice-points are the rubric.

## What it grades (over the diff)

For each addition in the diff, trace it to one of: the ticket's acceptance criterion, a design hook the
ticket names, a profile convention, or a decision record. Anything that traces to none is a finding:

- **Speculative abstraction** — a base class, protocol, generic, or plugin point with a single concrete
  use in this diff and no ticket that needs a second.
- **Unrequested options** — a parameter, flag, env var, or config key no input specified and no test
  exercises.
- **Surface the ticket did not name** — an endpoint, command, event, field, or page beyond the criterion.
- **Layering beyond the hook** — the design hook names a query guard; the diff adds a context object, a
  registry, and a factory around it.
- **Scope creep in existing code** — renames, reformatting, or refactors of lines the ticket did not
  touch (the auto-fix arm owns mechanical reformatting; anything else is a separate ticket).
- **Defensive code for impossible states** — handling for inputs the type system or the boundary
  already excludes.

## What it does NOT flag

- Anything a **profile convention** requires (a structured log event, a migration, the per-endpoint test
  matrix) — required is not extra.
- Anything a **decision record** in this build justifies.
- Tests. A test the ticket did not ask for is never a simplicity finding.
- The **negative case** a false-green trap demands (asserting the draft is *absent*) — that is the
  feature grader's requirement, not scope creep.

## Profile hooks

- **`rubrics.simplicity`** *(must)* — what "in scope" traces to in this domain: normally the ticket's
  criterion + hooks + the profile's declared choice-points. A profile may add domain items that are
  always in scope (e.g. "every endpoint owes its 401/404/422 handlers").

## Contract

```
grade(diff, rubric=<ticket criterion + hooks + choice-points>, context)
  → { pass, findings: [{file, line, added: <what>, traces_to: none, fix: remove | split-to-ticket}] }
```

- **pass** = every non-test addition traces to a declared source.
- A finding's fix is one of two: **remove** it, or **split it to a backlog ticket** with its own
  acceptance criterion (so the next agent builds it on purpose, graded).
- Runs in the parallel grader beat alongside feature · drift · docs-currency
  ([`skills/review-gate`](../skills/review-gate/SKILL.md)). Counts toward the shared ~4 budget.

## Relation to drift

**Drift** asks: did the diff apply what the profile and the hooks *require*? **Simplicity** asks: did the
diff add what nothing *requested*? A diff can pass drift (every required guard present) and fail
simplicity (three unrequested helpers around the guard). Keeping them separate keeps each rubric short;
folding simplicity into drift is the fallback if the composed set has to shrink.

> **Provenance:** ported from the DTS harness (2026-09), where it was the first grader added after the
> July split — nothing else in the loop catches over-building, and it was the most repeated manual
> correction. Ported with the two-fix rule (remove or split-to-ticket) intact.
