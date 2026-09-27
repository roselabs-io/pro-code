---
consumed_by: [orchestrator]
canonical_for: checks vs graders, and the deterministic tier in order
profile: agnostic
---

# checks — the deterministic tier

This directory holds the **checks**: tools and scripts that run over a diff and return facts. The other
kind of sensor, a **grader**, lives under [`graders/`](../graders/). The two words are not interchangeable,
and this file is where the distinction is defined; every other document links here rather than restating it.

## Checks vs graders

| | **Check** | **Grader** |
|---|---|---|
| What runs | a command or script | an LLM sub-agent, fresh context |
| Input | `diff` + a **config** row from the active profile's `check-commands.md` | `diff` + a **rubric** text the orchestrator injects |
| Output | `{ pass, findings }` — facts | `{ pass, findings, fix? }` — judgment |
| A pass means | proof | an opinion (which is why the core promise gets an N-vote) |
| Cost | cheap, reproducible, cacheable | expensive; frontier model |
| Order | first, in the order below, **short-circuit** | after every check is green, **in parallel** |
| Author ≠ grader | meaningless — a linter has no author to be biased by | enforced |
| How a profile adds one | a row in `check-commands.md` | a `.md` unit in `profiles/<x>/graders/` |
| Budget | unlimited | ~4 shared, +1 per personal overlay |
| Files | `checks/*.md`, `checks/doctrine_lint.py` | `graders/*.md`, `profiles/*/graders/*.md` |
| Contract | `check(diff, config, context)` | `grade(diff, rubric, context)` |

The orchestrator that runs both is [`skills/review-gate`](../skills/review-gate/SKILL.md). The gate
policy (what blocks) is stated there, once.

## The deterministic tier, in order

One ordered list. `check-commands.md` in a profile names the same checks by these row names; the
orchestrator runs them in this order and stops at the first red. A profile that does not run a check
declares it **n/a with a reason** in its `check-commands.md`; an undeclared absence is a GATE-0 finding.

| # | Check | Spec | Gated by | What it asserts |
|---|---|---|---|---|
| 0 | auto-fix arm | [`../codemods/README.md`](../codemods/README.md) | — | not a check: `ruff --fix` / `eslint --fix` / the profile's codemods run first so mechanical drift never becomes a finding |
| 1 | lint | row in `check-commands.md` | — | no violations |
| 2 | type-check | row in `check-commands.md` | — | no errors (a profile may declare it advisory) |
| 3 | doctrine-lint | [`doctrine_lint.py`](doctrine_lint.py) | — | comment doctrine regex subset · test-posture floor · the profile's `--forbid` rules (special-lint) |
| 4 | codemod-check | [`../codemods/README.md`](../codemods/README.md) | profile has a codemod | the codemod's `--check` reports nothing to rewrite |
| 5 | security | [`security.md`](security.md) | — | no secret in the diff (hard fail) · no high-severity SAST finding |
| 6 | tests | row in `check-commands.md` | — | zero failures, this session — the verify gate |
| 7 | coverage | [`coverage.md`](coverage.md) | — | changed lines covered ≥ the profile floor; no regression; no untested change |
| 8 | deps | [`dependencies.md`](dependencies.md) | — | no critical vuln in the shipped tree · lockfile consistent · license allowed |
| 9 | schema-validation | row in `check-commands.md` | profile declares one | output matches the contract |
| 10 | logs | [`../doc-patterns/harness/log-taxonomy.md`](../doc-patterns/harness/log-taxonomy.md) | — | the required structured events fired on a replayed run |
| 11 | runtime-smoke | [`runtime-smoke.md`](runtime-smoke.md) | `deploys: false` | the app boots from the README's launch command and answers one request |
| 12 | browser | [`browser.md`](browser.md) | `has_ui: true` | Playwright asserts the visual invariant on the rendered DOM of the running app |
| 13 | infra | [`infra.md`](infra.md) | `deploys: true` | images build · stack healthy on a fresh volume · migrations from empty · smoke through the proxy |

Rows 11–13 are the **runtime floor**: something boots and is observed. Which row applies is decided by
the two profile flags, never by omission — `deploys: true` runs infra (which subsumes runtime-smoke);
`deploys: false` runs runtime-smoke; `has_ui: true` adds browser on top of either.

This table is the only place the order is written. [`skills/review-gate`](../skills/review-gate/SKILL.md),
[`../COLD-REBUILD.md`](../COLD-REBUILD.md), the profile skeleton, and the harness `justfile` all point here.

## Active-profile resolution

Every check reads its row from `profiles/<active-profile>/check-commands.md`. The active profile is
resolved once per run, per [`../profiles/CONTRACT.md`](../profiles/CONTRACT.md#active-profile-resolution):
`$PROFILE` if set, else the project's `.pipeline-profile` file. There is no default; an unresolved
profile is a GATE-0 failure.

## Two rules every check follows

- **A missing precondition is a finding, not a pass.** No test at all, no scanner configured, no
  Dockerfile, no launch command — each is reported, never silently skipped.
- **Scoped to the diff** where the check has a diff to scope to (coverage, deps, security); whole-repo
  runs are periodic jobs, not per-ticket gates.
