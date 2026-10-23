---
consumed_by: ["grader:profile"]
canonical_for: "the review lens unit skeleton"
profile: _skeleton
---

# {lens-name} — profile-authored review lens unit

A review lens a **profile** ships (domain or personal). The one review of each ticket applies it after the
agnostic lenses of [`../../graders/review.md`](../../graders/review.md), in the same session and pass.
Copy into `profiles/<profile>/graders/<lens-name>.md` and fill it.

A lens unit is always **LLM judgment**. Add one only for a judgment the agnostic lenses and the profile's
`rubrics` do not already cover. If what you want to enforce is mechanical (a regex, a script, a command
exit code), it is not a lens: add a **row to `check-commands.md`** instead (a `--forbid`, a codemod
`--check`). Check rows are unlimited.

## rubric_source *(must)*
Where the lens judges against. **The orchestrator reads this and injects it into the review's prompt**
(the review session does not have the repo's docs in context — never write "go read X").
- {TODO: inline rubric text, OR a path in this profile the orchestrator injects}

## what it checks *(must)*
{TODO: the one focused thing on the diff this lens asserts. "handle X well" is not checkable — write an
assertion.}

## contract
```
findings for lens <lens-name>: [{file, line, issue, fix}]
```
- **pass** = {TODO: the condition}
- a **missing precondition** (no tests / no schema / no rendered surface) is a *finding*, not a silent pass.

## authoring discipline
One clear responsibility, not overlapping an agnostic lens. If two lenses would flag the same class of
thing, make it one.
