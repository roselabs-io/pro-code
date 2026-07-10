# {grader-name} — profile-authored grader unit

A grader a **profile** ships (domain or personal), discovered and run alongside the agnostic graders.
Copy into `profiles/<profile>/graders/<grader-name>.md` and fill it. Must conform to the grader contract
in [`../../graders/code-verification-loop.md`](../../graders/code-verification-loop.md).

## kind *(must)*
`deterministic` | `fuzzy`
- **deterministic** — a command/script; returns facts; runs first; short-circuits; no LLM. Unlimited.
- **fuzzy** — a fresh sub-agent, one rubric. Counts against the ~3 fuzzy budget (agnostic + domain +
  personal combined) — justify it, or fold it into an existing lens.

## rubric_source *(must)*
Where the grader judges against. **The orchestrator reads this and injects it into the sub-agent's
prompt** (sub-agents don't have the repo in context — never write "go read X").
- {TODO: inline rubric text, OR a path in this profile the orchestrator injects}

## what it checks *(must)*
{TODO: the one focused thing on the diff this grader asserts. "handle X well" is not checkable — write an
assertion.}

## contract
```
grade(diff, rubric=<above>, context) → { pass, findings: [{file, line, issue, fix}], fix? }
```
- **pass** = {TODO: the condition}
- a **missing precondition** (no tests / no schema / no rendered surface) is a *finding*, not a silent pass.

## authoring discipline
Few, focused, non-overlapping — one clear responsibility, same bar as the agnostic graders. If two fuzzy
graders would flag the same class of thing, make it one. (Deterministic checks are cheap — add as many as
there are mechanical rules; the ~3 cap is for the fuzzy ones only.)
