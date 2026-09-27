---
consumed_by: [grader:profile]
canonical_for: the grader unit skeleton
profile: _skeleton
---

# {grader-name} — profile-authored grader unit

A grader a **profile** ships (domain or personal), discovered and run alongside the agnostic graders.
Copy into `profiles/<profile>/graders/<grader-name>.md` and fill it. Must conform to the grader contract
in [`../../checks/README.md`](../../checks/README.md#checks-vs-graders).

A grader unit is always **LLM judgment** — a fresh sub-agent, one rubric. It counts against the ~4
shared budget (agnostic + domain; a personal overlay's unit is a +1) — justify it, or fold it into an
existing lens. If what you want to enforce is mechanical (a regex, a script, a command exit code), it is
not a grader: add a **row to `check-commands.md`** instead (a `--forbid`, a codemod `--check`). Check
rows are unlimited.

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
Few, focused, non-overlapping — one clear responsibility, same bar as the agnostic graders. If two
graders would flag the same class of thing, make it one.
