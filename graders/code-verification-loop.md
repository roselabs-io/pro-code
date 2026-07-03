# Grader — code-verification-loop

The **third** grader in the pipeline — the Implement→done gate — and the **keystone**. Frame and Plan grade the *context* (is the intent complete? does the plan cover it?); this one grades the **code** (does it match acceptance, run, not drift, leave the docs current?). Guidance *suggests* the how; a grader *enforces* it, and that jump is what takes a first materialization from ~40% on-target to ~90%.

Agnostic by design. The **loop, the contract, and the roster shape** below are domain-neutral; the **rubrics** (the actual conventions, the test/lint/type commands, the false-green traps) are supplied by the active profile. You're shipping *pytest, not the tests* — the empty machine + contract + playbook is the product.

## Why guidance isn't enough

A rule injected at the top of a long generation is a *suggestion*, and suggestions **dilute** as the agent burns context writing hundreds of lines. By the time it's deep in the work, the rule's traps have fallen out of attention, and nothing checks it afterward — so whatever it drifted into is what you get. The fix isn't better guidance. It's a **gate after the fact.**

## The loop

```
implement → [ parallel graders ] → collect ALL findings → ONE fix pass → re-grade
            ↑_________________________ until green / max-iter / stall _________________|
        → handoff (residual only)
```

## Two rules that make it work

- **Author ≠ grader.** The agent that wrote the code must not grade it — self-grading is lenient and blind to its own assumptions. **Fresh sub-agent, fresh context, one rubric in hand.** (The name for the kernel: *GAN-inspired* — a generator and an adversarial critic, specialized and separated. Borrow the structure, not the literal training; same reason a human can't review their own PR well.)
- **Fan out in parallel → collect ALL findings → ONE fix pass → re-grade.** Don't fix lens-by-lens; the fixes conflict and you waste passes. Gather everything, fix once, re-check. Each cycle climbs: ~40 → ~70 → ~90.

## The grader contract

Every grader — deterministic or fuzzy — is the same shape:

```
(diff, rubric-doc, context) → { pass: bool, findings: [...], fix: suggestion }
```

The domain lives in the **rubric-doc** (a profile-supplied text), not in the grader code — so most apparent domain-specificity is *parameterizable*. Ship the graders that take the rubric as input; the profile brings the rubric.

## The roster — split by kind

Not one multi-lens grader, and not a dozen fuzzy ones: **an auto-fix arm, then many cheap deterministic checks, then ~3 focused fuzzy graders.**

**0. The auto-fix arm (codemods) — runs FIRST, before any grader spends a finding.** A mechanical drift a script can fix should never reach a grader as a finding. Two tiers ([`codemods/`](../codemods/README.md)): **codemod-lite** (`ruff --fix`, `ruff format`, `eslint --fix`) every gate; **codemods** (libcst / ast-grep AST transforms) for a semantic bulk change a linter can't do. Deterministic, idempotent. When the drift grader keeps flagging the same mechanical thing, that's the signal to write a codemod for it.

**1. Deterministic checks — as many as you have mechanical rules.** Tools/scripts, not LLM graders — cheap, fast, reliable. **Run them ALL first; they short-circuit** (no point spending a fuzzy token on code that doesn't type-check):
- **type-check** (LSP-backed — pyright/mypy/tsc; semantic facts, not just style) · **lint** · **tests** (the verify gate) · **schema-validation** · **doctrine-lint** · **logs grader** — whatever the domain makes mechanical. The profile supplies the commands.
- **Doctrine-lint** ([`graders/checks/doctrine_lint.py`](checks/doctrine_lint.py)) — the deterministic **special-lint**: the regex-able subset of the **comment doctrine** (`doc-patterns/doctrines/comment-doctrine.md`), the **test-posture floor** (`doc-patterns/doctrines/test-posture.md` — every test asserts, no silent skip), and the profile's domain **`--forbid`** rules (`no-print`, `severity-constant`, …). The judgment cases stay with the drift grader; this is the mechanical floor.
- **Logs grader** ([`doc-patterns/harness/log-taxonomy.md`](../doc-patterns/harness/log-taxonomy.md)) — replays a run and asserts the right **structured events** fired: `HANDLER_RAN`, `CROSS_TENANT_DENIED`, `ALERT_RAISED{severity:critical}`. Proves the behaviour from the *trace*, not the return value — the deterministic answer to "200 ≠ the handler ran."
- **Browser grader** ([`graders/browser-grader.md`](browser-grader.md)) — for UI-bearing profiles only: Playwright drives the *running* app and asserts on the rendered DOM (the stale row shows "— stale", not a number). The only grader that sees what the user sees; runs in the verify beat after the API tests are green.

**2. Fuzzy graders — ~3, focused.** Each an expensive **fresh, isolated sub-agent** (author ≠ grader, enforced — not the authoring agent judging itself); keep them few or they just *blur*:
1. **Feature / spec** — does the diff satisfy the ticket's acceptance criterion? *(completeness)*
2. **Pattern / drift** — did it apply the ticket's design hooks + the profile's conventions? Reads the rubric's traps against the diff. Includes the **undeclared-choice lens**: does the diff pick a library, tool, config, pattern, or naming that *no input specified* and the profile's **choice-points** don't cover? Every such silent default is surfaced to `docs/assumptions.md` with a disposition (promote to the profile / log as a decision / flag to the driver / accept). This is the guard against the agent's own priors leaking in unseen. *(quality)*
3. **Docs-currency** — did it maintain the living docs? Backlog pruned + forward-only, a decision record for any new decision, current-state + open-questions updated, **the assumptions ledger current** (every silent choice dispositioned). **Context is a first-class artifact — grade it like code.** *(context)*

**Run the fuzzy graders in PARALLEL** (concurrent sub-agents) → collect ALL findings → ONE fix pass → re-grade. On the **core-promise finding** — the one invariant that must not be wrong (isolation; no-missed-alert) — optionally run an **adversarial N-vote**: several isolated graders each try to *refute* it; it survives only on a majority. That's parallelization (sectioning + voting) inside the gate.

## The hierarchy — keep it straight

**correctness (verify) > completeness (feature) > quality (pattern/style) + context (docs-currency, gated separately).**

A pattern-perfect diff that doesn't run is still a fail. Never let pattern-policing wave through something broken — **pattern-compliance ≠ correctness.** And a run isn't "done" if it left the memory stale, so docs-currency gates in parallel: green code + poisoned docs is not a pass.

The **verify gate is the sacred arbiter** — the one that actually runs the code against the *real* acceptance criterion (not a proxy), this session. No fresh evidence, no pass.

## Stopping conditions (a loop with no ceiling is a blank check)

- **All graders green** → handoff. ✅
- **Max iterations (~3)** → handoff with the residual flagged. ⚠️
- **No progress** (the *same* finding recurs) → the agent can't fix it; **escalate to human.** A stall is *signal, not failure* — it's exactly the hard thing worth your attention.

## The handoff is the residual, not the whole

Not "here's 90%, go re-audit." It's *"all graders green except these 2 the loop couldn't resolve."* The human reviews the residual ~10%, not the entire diff — that's what removes the human as the bottleneck.

## Cost discipline

- **Deterministic graders first** — cheap, and they short-circuit before a fuzzy grader spends a token.
- **Frontier model only on the fuzzy judges;** a cheap model for mechanical lenses.
- **Prompt-cache the rubrics** — they re-send every iteration.
- **Hard-cap iterations** — treat a stall as a failure signal, not a reason to keep burning tokens.

## The principle that replaces you

> **Every piece of feedback you give twice is a missing grader.**

Repeated "did you use the pattern / why are these comments verbose" isn't feedback — it's a rubric living in your head. The moment you catch yourself restating a correction, **encode it as a grader rule**, not a one-off comment. The loop only replaces you for the corrections you've externalized — and recurring findings feed back to *strengthen the guide* (the conventions), so the next project starts at ~70 instead of ~40. Pain compounds into automation.

## Profile hooks

A profile supplies:
- **`deterministic_checks`** — the mechanical grader commands for this domain (type-check, lint, test, schema-validate, comment-doctrine).
- **`fuzzy_rubrics`** — what each of the ~3 fuzzy graders points at: the acceptance criterion (feature), the design catalog + conventions (drift), the living-docs set (docs-currency).
- **`verify_means`** — how you prove it *actually ran* in this domain, plus the **false-green traps** (the `200-but-the-handler-never-fired` class of lies that make a check pass while the behaviour is broken).

## Worked example (`generic-saas` — the multi-tenant isolation ticket)

```
Implement — T5 "Enforce tenant isolation on /projects"
acceptance: A's token GET /projects/{B_id} → 404; no tenant-B row ever serializes.
hook: tenant-scoped-query-guard

Iteration 1 — author's first cut lands ~40% on-target.
  DETERMINISTIC (run first, short-circuit)
    ✓ type-check   ✓ lint
    ✗ tests        — integration test `test_cross_tenant_404` FAILS: returns 200 + B's row.
       → short-circuits; don't spend fuzzy tokens yet. Fix pass.

Iteration 2 — after ONE fix pass (scoped the query by tenant).
  DETERMINISTIC  ✓ type-check ✓ lint ✓ tests (cross-tenant → 404, list excludes B)
  FUZZY (fresh sub-agent each, parallel)
    ✓ feature/spec  — criterion met: the failing assertions now pass.
    ✗ drift         — the guard is applied on GET but MISSING on PATCH /projects/{id};
                       tenant-scoped-query-guard says scope EVERY read/write. Deny-by-default absent.
    ✗ docs-currency — current-state.md still says "isolation: TODO"; no decision record for
                       the app-layer-vs-RLS choice.
  → collect BOTH, ONE fix pass.

Iteration 3 — re-grade. all green.
  ✓ deterministic ✓ feature ✓ drift (guard on all verbs, deny-by-default) ✓ docs-currency.
  → HANDOFF. Residual: none. (Had drift recurred a 3rd time → escalate, don't loop forever.)

Why this is the demo's payoff: "done" here is HARD (no cross-tenant leak), so the grader —
not the author's confidence — is what makes shipping it autonomously trustworthy. The verify
gate proved the 404 with a real test; the drift grader caught the half-applied guard the author
was blind to; docs-currency kept the next agent from inheriting "isolation: TODO" amnesia.
```
