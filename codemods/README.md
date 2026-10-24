---
consumed_by: ["build"]
canonical_for: "the auto-fix arm"
profile: agnostic
---

# codemods — the deterministic auto-fix arm

> **Code mods** (feedforward + auto-fix, ⚙️): AST-based **bulk transforms**
> that migrate once and apply to N files, deterministically. The auto-fix arm of
> review-gate — it runs *before* the checks and the review, so a mechanical drift is corrected
> by a script (cheap, exact, reviewable) instead of by tokens.

## Why it's first-class, not just `ruff --fix`

Two tiers, both in review-gate:

- **Codemod-lite** — a formatter + safe autofixer (`ruff --fix`, `ruff format`, `eslint --fix`). Fixes style/import/trivial drift. Runs every gate.
- **Codemod** — a real **AST transform** (libcst · ast-grep · ts-morph · jscodeshift) for a *semantic* bulk change a linter can't do: enforce a convention across every handler, migrate an API, rewrite a call shape. Authored once, applied to N files, re-runnable.

## The contract

A codemod is a script with a stable interface:

```
codemods/<name>.py  <path...>     # transform files in place (or --check to dry-run)
  → exits 0 and reports: N files scanned, M rewritten
  → idempotent: running twice changes nothing the second time
  → deterministic: same input → same output (no clock/random)
```

## Where it sits in review-gate

```
implement → [ ruff --fix + codemods ]  ← deterministic auto-fix arm (this dir) — stage 0
          → [ checks, in the order checks/README.md fixes, short-circuit ]
          → [ one review: feature · drift · docs-currency · simplicity ]  ← LLM, only if every check is green
          → at most one fix pass → checks rerun → handoff to the human
```

The auto-fix arm short-circuits the cheapest drift: **a convention a codemod can enforce should never reach the review as a finding.** If the review's drift lens keeps flagging the same mechanical thing, that's the signal to write a codemod for it (the "every correction given twice is a missing check" principle).

## What the plugin ships vs BYO

- **Ships (agnostic):** this contract + the review-gate stage (row 0 in [`../checks/README.md`](../checks/README.md#the-deterministic-tier-in-order); `codemod-check` is row 4) + the `just codemod <name>` entry point.
- **BYO (per example/profile):** the actual transforms — they encode *your* conventions. See each example's `codemods/`.
