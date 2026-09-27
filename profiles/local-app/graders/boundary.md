---
consumed_by: ["grader:boundary"]
canonical_for: "the `local-app` boundary rubric"
profile: local-app
---

# boundary — profile-authored grader unit (`local-app`)

The domain's core promise: nothing of the user's leaves the machine unredacted, and nothing raw is
written to disk. A deterministic leak test exists (the `logs` row and the per-ticket leak test);
this grader judges what a regex cannot — whether a diff *introduced* a path the tests do not cover.

## rubric_source *(must)*
Inline:
- Every network call in the diff is in the one egress module, and its input is the redacted text
  (trace the variable back to the gate's return value).
- Every file write in the diff is of redacted text, the mapping, a model, or a config value — never
  the ingested text, an audio buffer, or a clipboard read.
- Any new stage between ingest and the gate holds the raw text in memory only and does not log it
  (including in exceptions and `repr`).
- If the diff touches the gate, the mapping store, the trace writer or the egress module, a leak
  test in the diff ran this session and reports zero.

## what it checks *(must)*
That the diff adds no egress and no raw-input write, and that a boundary change comes with a leak
test that ran green.

## contract
```
grade(diff, rubric=<above>, context) → { pass, findings: [{file, line, issue, fix}], fix? }
```
- **pass** = no new egress outside the egress module · no raw-input write · boundary change ⇒ leak
  test present and green with fresh output.
- a **missing leak test** on a boundary change is a finding, not a silent pass.

## authoring discipline
One responsibility: the boundary. Format, drift and simplicity belong to the agnostic graders.
