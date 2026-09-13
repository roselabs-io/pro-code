---
name: review-gate
description: "Implement's gate — the code-verification loop. Run the auto-fix arm, then the checks in short-circuit order, then the graders as isolated sub-agents; collect all findings, fix once, re-grade until green, capped, or stalled. Composes the agnostic layer, the active domain profile, and an optional personal overlay."
---

# review-gate (the code-verification loop)

The **third** gate in the pipeline — Implement→done. Frame and Plan grade the *context* (is the intent complete? does the plan cover it?); this one gates the **code** (does it match acceptance, run, not drift, leave the docs current, and add nothing that wasn't asked for?). Guidance *suggests* the how; a gate *enforces* it, and that jump is what takes a first materialization from ~40% on-target to ~90%.

This skill is the **orchestrator**. It runs no check and holds no rubric of its own: the checks are specified under [`checks/`](../../checks/README.md), the graders under [`graders/`](../../graders/), and the commands, thresholds, and rubrics come from the **active profile** (resolved per [`profiles/CONTRACT.md`](../../profiles/CONTRACT.md#active-profile-resolution)). What ships is the machine and the two contracts, not the domain content: *pytest, not the tests*.

## Why guidance isn't enough

A rule injected at the top of a long generation is a *suggestion*, and suggestions **dilute** as the agent burns context writing hundreds of lines. By the time it's deep in the work, the rule's traps have fallen out of attention, and nothing checks it afterward — so whatever it drifted into is what you get. The fix isn't better guidance. It's a **gate after the fact.**

## The loop

```
implement → [ auto-fix arm ] → [ checks, in order, short-circuit ] → [ graders, parallel ]
            → collect ALL findings → ONE fix pass → re-run
            ↑______________________ until green / max-iter / stall ______________________|
        → handoff (residual only)
```

## Two rules that make it work

- **Author ≠ grader.** The agent that wrote the code must not grade it — self-grading is lenient and blind to its own assumptions. **Fresh sub-agent, fresh context, one rubric in hand.** (The name for the kernel: *GAN-inspired* — a generator and an adversarial critic, specialized and separated. Borrow the structure, not the literal training; same reason a human can't review their own PR well.) This rule is about graders. A check has no author to be biased by.
- **Fan out in parallel → collect ALL findings → ONE fix pass → re-grade.** Don't fix lens-by-lens; the fixes conflict and you waste passes. Gather everything, fix once, re-check. Each cycle climbs: ~40 → ~70 → ~90.

## Two contracts, not one

A **check** and a **grader** are different things and carry different words ([the table](../../checks/README.md#checks-vs-graders)):

```
check(diff, config, context)  → { pass, findings: [...] }        # a command; facts; proof
grade(diff, rubric, context)  → { pass, findings: [...], fix? }  # a sub-agent; judgment; opinion
```

The domain lives in the **config** (a profile's `check-commands.md` row) and the **rubric-doc** (a profile-supplied text), not in the loop — so most apparent domain-specificity is *parameterizable*. Ship the checks and graders that take those as input; the profile brings the content.

## The roster

Not one multi-lens grader, and not a dozen graders: **an auto-fix arm, then many cheap checks, then ~4 focused graders.**

**0. The auto-fix arm (codemods) — runs FIRST, before any check reports a finding.** A mechanical drift a script can fix should never reach a check or a grader as a finding. Two tiers ([`codemods/`](../../codemods/README.md)): **codemod-lite** (`ruff --fix`, `ruff format`, `eslint --fix`) every gate; **codemods** (libcst / ast-grep AST transforms) for a semantic bulk change a linter can't do. Deterministic, idempotent. When the drift grader keeps flagging the same mechanical thing, that's the signal to write a codemod for it.

**1. Checks — as many as you have mechanical rules.** Tools/scripts, not LLM judgment — cheap, fast, reproducible. **Run them ALL first, in the order [`checks/README.md`](../../checks/README.md#the-deterministic-tier-in-order) fixes; they short-circuit** (no point spending a grader token on code that doesn't type-check). The profile supplies the commands (`check-commands.md`); a check the domain doesn't run is **declared n/a** there, never silently dropped. Two checks are gated by a profile flag: **browser** by `has_ui`, **infra** by `deploys`; **runtime-smoke** covers the boots-at-all floor when `deploys` is false.

**2. Graders — ~4, focused.** Each an expensive **fresh, isolated sub-agent** (author ≠ grader, enforced — not the authoring agent judging itself); keep them few or they just *blur*:
1. **Feature / spec** — does the diff satisfy the ticket's acceptance criterion? *(completeness)*
2. **Pattern / drift** — did it apply the ticket's design hooks + the profile's conventions? Reads the rubric's traps against the diff. Includes the **undeclared-choice lens**: does the diff pick a library, tool, config, pattern, or naming that *no input specified* and the profile's **choice-points** don't cover? Every such silent default is surfaced to `docs/assumptions.md` with a disposition (promote to the profile / log as a decision / flag to the driver / accept). This is the guard against the agent's own priors leaking in unseen. *(quality)*
3. **Docs-currency** — did it maintain the living docs? Backlog pruned + forward-only, a decision record for any new decision, current-state + open-questions updated, **the assumptions ledger current** (every silent choice dispositioned). **Context is a first-class artifact — grade it like code.** *(context)*
4. **Simplicity** ([`graders/simplicity.md`](../../graders/simplicity.md)) — did it build *only* what the ticket asked for? An abstraction used once, an option nobody requested, a layer the design hook doesn't name, a "while I'm here" refactor — each is a finding, traced to the ticket line it does not serve. Drift asks "did you apply what was required?"; simplicity asks "did you add what wasn't?" *(scope)*

**Run the graders in PARALLEL** (concurrent sub-agents) → collect ALL findings → ONE fix pass → re-grade. On the **core-promise finding** — the one invariant that must not be wrong (isolation; no-missed-alert; no-draft-leak) — optionally run an **adversarial N-vote**: several isolated graders each try to *refute* it; it survives only on a majority. That's parallelization (sectioning + voting) inside the gate.

## Composition — how the layers combine

The gate composes, in order:
1. **agnostic checks and graders** (`checks/`, `graders/`) — always run;
2. **active domain profile** — its `check-commands.md` rows, rubrics, and any `profiles/<domain>/graders/`;
3. **optional personal overlay** — its *additional* rubric rows / forbids + `profiles/personal/<name>/graders/`.

Rubrics **union**; forbids **union**; grader sets **union**. On conflict the **stricter** rule wins — additive-only guarantees a personal overlay can only tighten. A profile-authored grader is always LLM judgment (it counts toward the ~4); a profile's deterministic rule is a **row in `check-commands.md`**, not a grader.

## Gate policy — what blocks

In pro-code **both checks and graders block**: a red check or a red grader means the ticket is not done, and the loop keeps going until green, capped, or stalled. A grader's verdict is an opinion, so the loop gives it one fix pass and a re-grade before it counts; a check's verdict is a fact and counts immediately. This is a solo-driver choice — one person owns every profile, so a grader that blocks is a grader that person wrote and can retune. A team running the same machinery may prefer graders that *report* and never block, keeping only the checks as hard gates; the loop supports that as a policy switch on the graders, not a structural change.

## The hierarchy — keep it straight

**correctness (verify) > completeness (feature) > quality (pattern/style) + scope (simplicity) + context (docs-currency, gated separately).**

A pattern-perfect diff that doesn't run is still a fail. Never let pattern-policing wave through something broken — **pattern-compliance ≠ correctness.** And a run isn't "done" if it left the memory stale, so docs-currency gates in parallel: green code + poisoned docs is not a pass.

**The verify gate decides.** It runs the code against the real acceptance criterion, not a proxy, in this session. No fresh evidence, no pass.

## Stopping conditions

- **All checks and graders green** → handoff. ✅
- **Max iterations (~3)** → handoff with the residual flagged. ⚠️
- **No progress** (the *same* finding recurs) → the agent can't fix it; **escalate to human.** A stall is *signal, not failure* — it's exactly the hard thing worth your attention.

## The handoff is the residual, not the whole

Not "here's 90%, go re-audit." It's *"all green except these 2 the loop couldn't resolve."* The human reviews the residual ~10%, not the entire diff — that's what removes the human as the bottleneck.

## Cost discipline

- **Checks first** — cheap, and they short-circuit before a grader spends a token.
- **Frontier model only on the graders;** a cheap model, or none, for the mechanical lenses.
- **Prompt-cache the rubrics** — they re-send every iteration.
- **Hard-cap iterations** — treat a stall as a failure signal, not a reason to keep burning tokens.

## The principle that replaces you

> **Every piece of feedback you give twice is a missing check or grader.**

Repeated "did you use the pattern / why are these comments verbose" isn't feedback — it's a rubric living in your head. The moment you catch yourself restating a correction, **encode it** — as a `--forbid` row or a codemod if it's mechanical, as a grader rubric line if it's judgment — not as a one-off comment. The loop only replaces you for the corrections you've externalized — and recurring findings feed back to *strengthen the guide* (the conventions), so the next project starts at ~70 instead of ~40. Pain compounds into automation.

## Profile hooks

A profile supplies (the full list: [`profiles/CONTRACT.md`](../../profiles/CONTRACT.md)):
- **`check_commands`** — one row per check this domain runs, with command + threshold + allowlist (`check-commands.md`); n/a rows say why.
- **`rubrics`** — what each of the ~4 graders points at: the acceptance criterion (feature), the design catalog + conventions (drift), the living-docs set (docs-currency), the ticket scope + declared choice-points (simplicity).
- **`verify_means`** — how you prove it *actually ran* in this domain, plus the **false-green traps** (the `200-but-the-handler-never-fired` class of lies that make a check pass while the behaviour is broken).

## Worked example (`generic-saas` — the multi-tenant isolation ticket)

```
Implement — T5 "Enforce tenant isolation on /projects"
acceptance: A's token GET /projects/{B_id} → 404; no tenant-B row ever serializes.
hook: tenant-scoped-query-guard

Iteration 1 — author's first cut lands ~40% on-target.
  CHECKS (run first, short-circuit)
    ✓ type-check   ✓ lint
    ✗ tests        — integration test `test_cross_tenant_404` FAILS: returns 200 + B's row.
       → short-circuits; don't spend grader tokens yet. Fix pass.

Iteration 2 — after ONE fix pass (scoped the query by tenant).
  CHECKS   ✓ type-check ✓ lint ✓ tests (cross-tenant → 404, list excludes B) ✓ smoke
  GRADERS (fresh sub-agent each, parallel)
    ✓ feature/spec  — criterion met: the failing assertions now pass.
    ✗ drift         — the guard is applied on GET but MISSING on PATCH /projects/{id};
                       tenant-scoped-query-guard says scope EVERY read/write. Deny-by-default absent.
    ✗ docs-currency — current-state.md still says "isolation: TODO"; no decision record for
                       the app-layer-vs-RLS choice.
    ✗ simplicity    — a `TenantContext` class with 4 methods, 1 used; the hook names a query guard,
                       not a context object.
  → collect ALL, ONE fix pass.

Iteration 3 — re-grade. all green.
  ✓ checks ✓ feature ✓ drift (guard on all verbs, deny-by-default) ✓ docs-currency ✓ simplicity.
  → HANDOFF. Residual: none. (Had drift recurred a 3rd time → escalate, don't loop forever.)

Why this is the demo's payoff: "done" here is HARD (no cross-tenant leak), so the gate —
not the author's confidence — is what makes shipping it autonomously trustworthy. The verify
check proved the 404 with a real test; the drift grader caught the half-applied guard the author
was blind to; docs-currency kept the next agent from inheriting "isolation: TODO" amnesia.
```
