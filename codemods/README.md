# codemods — the deterministic auto-fix arm

> **Code mods** (feedforward + auto-fix, ⚙️): AST-based **bulk transforms**
> that migrate once and apply to N files, deterministically. The auto-fix arm of the
> verification loop — it runs *before* the LLM fix pass, so a mechanical drift is corrected
> by a script (cheap, exact, reviewable) instead of by tokens.

## Why it's first-class, not just `ruff --fix`

Two tiers, both in the loop:

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

## Where it sits in the verification loop

```
implement → [ ruff --fix + codemods ]  ← deterministic auto-fix arm (this dir)
          → [ deterministic graders: lint · type · logs · test ]
          → [ fuzzy graders: feature · drift · docs-currency ]  ← LLM, only if needed
          → fix pass → re-grade
```

The auto-fix arm short-circuits the cheapest drift: **a convention a codemod can enforce should never reach a fuzzy grader as a finding.** If the drift grader keeps flagging the same mechanical thing, that's the signal to write a codemod for it (the "every correction twice is a missing grader" principle, applied to the deterministic side).

## What the plugin ships vs BYO

- **Ships (agnostic):** this contract + the loop stage + the `just codemod <name>` entry point.
- **BYO (per example/profile):** the actual transforms — they encode *your* conventions. See each example's `codemods/`.
